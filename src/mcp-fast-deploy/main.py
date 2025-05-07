from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, ValidationError, field_validator
import json
import fc_utils
from log import LOGGER

app = FastAPI(title="MCP 服务管理系统")

# 挂载静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 部署地域选项
REGIONS = [
    {"label": "华东1（杭州）", "value": "cn-hangzhou"},
    {"label": "华北2（北京）", "value": "cn-beijing"},
    {"label": "华东2（上海）", "value": "cn-shanghai"},
    {"label": "华南1（深圳）", "value": "cn-shenzhen"},
    {"label": "新加坡", "value": "ap-southeast-1"},
]


# Pydantic 数据模型
class McpConfig(BaseModel):
    timeout: int = 30
    memory: int = 512
    environment: dict = {}


class McpCreateRequest(BaseModel):
    name: str
    region: str
    install_method: str
    config: McpConfig  # 嵌套模型验证

    @field_validator("install_method")
    def validate_install_method(cls, v):
        if v not in ["npx", "uvx"]:
            raise ValueError("安装方式必须是 npx 或 uvx")
        return v


# 路由定义
@app.get("/")
async def create_page(request: Request):
    return templates.TemplateResponse(
        "mcp_create.html", {"request": request, "regions": REGIONS}
    )


@app.post("/api/mcp-services")
async def create_service(
    name: str = Form(...),
    description: str = Form(...),
    region: str = Form(...),
    install_method: str = Form(...),
    config: str = Form(...),
):
    try:
        LOGGER.info(
            f"name ={name}, description={description}, region={region}, install_method={install_method}, config={config}"
        )
        r = extract_params(config)
        LOGGER.info(r)

        cmd_str = r["command"] + " " + " ".join(r["args"])
        LOGGER.info(cmd_str)
        if r["command"] == "npx":
            assert cmd_str.startswith("npx -y")

        ret = await fc_utils.handler(
            cmd=cmd_str, envs=r["env"], name=name, desc=description
        )

        # 模拟生成端点信息
        return {
            "status": "success",
            "data": {"endpoint": ret["endpoint"], "functionArn": ret["functionArn"]},
        }

    except json.JSONDecodeError as e:
        raise HTTPException(422, detail=f"JSON格式错误：{e.msg}")
    except ValidationError as e:
        raise HTTPException(422, detail=e.errors())
    except Exception as e:
        raise HTTPException(422, detail=f"其他错误：{e.msg}")


def extract_params(json_str: str) -> dict:
    """从 MCP 服务配置中提取核心参数"""
    config = json.loads(json_str)

    # 获取第一个服务的配置（每个配置只有一个服务）
    service_name = next(iter(config["mcpServers"]))
    service_config = config["mcpServers"][service_name]

    return {
        "command": service_config["command"],
        "args": service_config.get("args", []),
        "env": service_config.get("env", {}),
    }
