
> 注：当前项目为 Serverless Devs 应用，由于应用中会存在需要初始化才可运行的变量（例如应用部署地区、函数名等等），所以**不推荐**直接 Clone 本仓库到本地进行部署或直接复制 s.yaml 使用，**强烈推荐**通过 `s init ${模版名称}` 的方法或应用中心进行初始化，详情可参考[部署 & 体验](#部署--体验) 。

# start-mcp-fast-deploy 帮助文档

<description>

STDIO MCP服务通过函数计算 FC 一键部署转型为 SSE 远程服务

</description>


## 资源准备

使用该项目，您需要有开通以下服务并拥有对应权限：

<service>



| 服务/业务 |  权限  | 相关文档 |
| --- |  --- | --- |
| 函数计算 |  AliyunFCFullAccess | [帮助文档](https://help.aliyun.com/product/2508973.html) [计费文档](https://help.aliyun.com/document_detail/2512928.html) |
| 日志服务 |  AliyunFCServerlessDevsRolePolicy | [帮助文档](https://help.aliyun.com/zh/sls) [计费文档](https://help.aliyun.com/zh/sls/product-overview/billing) |

</service>

<remark>



</remark>

<disclaimers>



</disclaimers>

## 部署 & 体验

<appcenter>
   
- :fire: 通过 [云原生应用开发平台 CAP](https://cap.console.aliyun.com/template-detail?template=start-mcp-fast-deploy) ，[![Deploy with Severless Devs](https://img.alicdn.com/imgextra/i1/O1CN01w5RFbX1v45s8TIXPz_!!6000000006118-55-tps-95-28.svg)](https://cap.console.aliyun.com/template-detail?template=start-mcp-fast-deploy) 该应用。
   
</appcenter>
<deploy>
    
   
</deploy>

## 案例介绍

<appdetail id="flushContent">

在当前市面已经公开的各种 MCP Server,  基本都是基于 STDIO 的实现，并且打包为独立的二进制可执行文件进行分发。其中 Node.js  和 python 占据了绝大多数，Node.js 生态通常通过 npx 提供，例如 "npx -y @amap/amap-maps-mcp-server"， Python 生态则以 uvx 提供, 例如 "uvx mcp-server-time --local-timezone=Asia/Shanghai"， 因此，将社区主流 STDIO MCP  Server 一键转为自己 的 MCP Server 是一个非常有价值的事情， 本案例展示STDIO MCP服务通过函数计算 FC 一键部署转型为 SSE 远程服务。

</appdetail>




## 架构图

<framework id="flushContent">

![](https://img.alicdn.com/imgextra/i2/O1CN01behcGo1ppNNH39W9p_!!6000000005409-2-tps-1500-1040.png)

</framework>

## 使用流程

<usedetail id="flushContent">

部署成功后：

1. 打开这个 web 应用，可以选择 npx 或者 uvx 部署,
  a.  我们以 高德地图@amap/amap-maps-mcp-server 为例
  b.  填写完毕，点击 "提交部署" 按钮,  等待一会， 会显示部署成功，并会显示部署成功以后保留的 mcp 服务 url 和支持这个 MCP  服务计算资源的函数 ARN

    ![](https://img.alicdn.com/imgextra/i3/O1CN01080uah25QfrgsxrAS_!!6000000007521-2-tps-1136-1664.png)

2. 直接使用 "npx @modelcontextprotocol/inspector" 调试器调试部署成功的 MCP SSE 服务
    
    ![](https://img.alicdn.com/imgextra/i3/O1CN01hhyMWk1eKGhSdOCJ8_!!6000000003852-2-tps-1240-578.png)


3. 之后，就可以把这个 url 注册到各种 Agent 客户端去消费， 比如百练、 Cherry Studio 等， 以 Cherry Studio 为例

    ![](https://img.alicdn.com/imgextra/i4/O1CN01xbSZbv1EnsID7uVEL_!!6000000000397-2-tps-1256-863.png)
    ![](https://img.alicdn.com/imgextra/i2/O1CN01ZDeyag2ALhe4GAvV0_!!6000000008187-2-tps-1252-854.png)

</usedetail>

## 二次开发指南

<development id="flushContent">

您可以根据您的需求基于 https://github.com/devsapp/mcp-fast-deploy  进行二次开发

</development>






