# pyweb-dev-tools

### 项目简介

pyweb-dev-tools是使用pyqt+vue开发的实用工具脚手架，利用业余时间把工作中遇到的一些问题总结起来，打包进小工具集中，供大家在程序开发过程中参考和使用，同时支持二次开发，只要会python+web基础，就能进行自定义的工具集开发，开发好的工具集可以提交到工具集仓库，然后发布分享给其他用户，不断扩展转达工具集功能。

每一个工具集可以用web开发开发界面实现一些功能，在web开发不满足条件情况下，比如需要获取设备能力时，可以使用python定义后端接口函数，插件按命名空间封装了web端和python端的通信，js很方便进行调用python函数

### 项目示例图

![输入图片说明](https://images.gitee.com/uploads/images/2020/0110/104755_159f314b_1009390.png "项目示例图.png")

### 支持平台 

支持window，mac平台



### 环境安装

#### 1 安装python环境 3.7版本或以上

#### 2 安装nodejs环境 10.8版本或以上



### 开始开发 

本项目为插件开发脚手架，已上传到pypi仓库 无需手工安装

以下为基于该脚手架的插件二次开发步骤



##### 1 新建一个插件工程 

工程以获取系统cpu序列号和mac地址为例，以下均以该工程做示例，实际可自定义

工程名 plugin_sys_info

##### 2 根目录初始化前端项目

以vue为例，初始化vue项目 **vue init webpack vuedev**

调整打包配置项 vuedev/config/index.js 修改如下代码便于打包

```javascript
build：{
    index: path.resolve(__dirname, '../dist/index.html'), //改为../dist/index.html
    // Paths
    assetsRoot: path.resolve(__dirname, '../dist'), //改为../
    assetsSubDirectory: 'static',
    assetsPublicPath: './', //改为./
//other
}
```

> 建议使用iview管理端框架统一样式

安装 qt-channel 用于javascript调用后端python接口 ，如果无需调用python后台可不添加

```bat
npm qt-channel vue -S
```

##### 3 创建插件配置文件

根目录新建一个 config.ini 配置文件，添加如下配置：

```ini
[base]
;前端项目IP地址
webpack_server_ip = localhost 
;前端项目端口
webpack_server_port = 8080
;前端项目根目录
webpack_root_path = /vuedev
;前端项目插件目录
webpack_plugin_path = /src/plugin
```

##### 4 安装python依赖

新建依赖配置文件 requirements.txt，添加如下内容 ：

```
PyQt5==5.13.2
PyQtWebEngine==5.13.2
requests==2.22.0
PyInstaller==3.5
numpy==1.16.4
pywin32==224
wmi==1.4.9
pyweb-dev-tools==0.0.2
```

> pyweb-dev-tools==0.0.2 为插件脚手架版本，后边会不定期更新 可在pypi搜索

根目录执行依赖安装命令：

```bat
pip install pipreqs && pip install -r requirements.txt
```

##### 5 创建python启动脚本

根目录新建一个 app.py 配置文件，添加如下配置：

```python
# -*- coding: utf-8 -*-
from pyWebDevTool.main import App

if __name__ == "__main__":    
    App()
```

至此 脚手架已经搭建完毕，运行该脚本，程序启动如下

![首页](https://images.gitee.com/uploads/images/2020/0110/093052_fdcc52b3_1009390.png "首页.png")

##### 6 插件模块开发

在脚手架基础上，可以进行插件工具的开发



###### 6.1 插件属性定义

vuedev/src/plugin目录下 新建python包（注意是python包不是目录，需要包含________init________.py）, 建议安装公司名+项目名结构命名

例如 vuedev/src/plugin/com/github/luanhy/sysinfo

新建一个插件属性定义文件 package-info.js

```javascript
export default {
  "groupId": "com.github.luanhy",//公司名
  "artifactId": "sysinfo",//项目名
  "version": "1.0.0",//版本号
  "router": "router.py",//后端入口文件
  "indexPath": "/",//前端入口路径
  "name": "系统信息获取工具",//项目名称
  "description": "包含mac地址获取和cpu信息获取",//项目描述
  "class": "系统工具" //项目分类
}
```

###### 6.2 插件后台开发

如果需要调用后台
vuedev/src/plugin/com/github/luanhy/sysinfo目录添加后台路由router.py文件，示例为定义获取mac地址和cpu序列号的函数接口

```python
# -*- coding: utf-8 -*-
from pyWebDevTool.router.routeContext import rc

import wmi

from pyWebDevTool.util.loggerFactory import Logger

logger = Logger()

__sys_info = {
  "cpuCode": None,
  "mac": None
}


@rc.route("/get_mac")
def get_mac(params):
  """获取本机mac地址"""
  return getMac()


@rc.route("/get_cpu_info")
def get_cpu_info(params):
  """获取设备CPU序列号"""
  return getCpuCode()


def __getCpuCode():
  """获取cpu序列号多个竖线分隔"""
  cpuId = ""
  for processor in wmi.WMI().Win32_Processor():
    cpuId += processor.ProcessorId.strip() + "|"
  return cpuId[0: len(cpuId) - 1]


def getCpuCode():
  cpuCode = __sys_info['cpuCode']
  if cpuCode is None:
    cpuCode = __getCpuCode()
    logger.info("获取到的cpu序列号为：%s" % cpuCode)
    __sys_info['cpuCode'] = cpuCode
  return cpuCode


def getMac():
  mac = __sys_info['mac']
  if mac is None:
    mac = __getMac()
    logger.info("获取到的mac地址为：%s" % mac)
    __sys_info['mac'] = mac
  return mac


def __getMac():
  """获取mac地址多个竖线分隔"""
  macs = ""
  for mac in wmi.WMI().Win32_NetworkAdapter():
    if mac.MACAddress is not None:
      macs += mac.MACAddress + "|"
  return macs[0: len(macs) - 1]

```

###### 6.3 插件前端开发

 vuedev/src/plugin/com/github/luanhy/sysinfo/web/目录 创建vue页面文件index.vue

```vue
<template>
  <div style="padding: 20px">
    <div>
      <button @click="getMac" :disabled="disabled">获取MAC地址</button>
      你的MAC地址是:<br>
      <input v-model="msg" style="width: 100%;"/>
    </div>
    <div>
      <button @click="getCpuInfo" :disabled="disabled">获取CPU序列号</button>
      你的PC CPU序列号是:<br>
      <input v-model="cpuMsg" style="width: 100%;"/>
    </div>
  </div>
</template>

<script>

  import {QtRequest} from 'qt-channel'
  import packageInfo from "../package-info"

  export default {
    name: "sysInfo",
    data() {
      return {
        msg: '',
        cpuMsg: "",
        disabled: false
      }
    },
    mounted() {
      console.log(packageInfo)
    },
    methods: {
      async getMac() {
        this.disabled = true
        this.msg = await QtRequest({
          path: "/get_mac",//此处和后台router.py的router路径相对应
          packageInfo,
        })
        this.disabled = false
      },
      async getCpuInfo() {
        this.disabled = true
        this.cpuMsg = await QtRequest({
          path: "/get_cpu_info",//此处和后台router.py的router路径相对应
          packageInfo,
        })
        this.disabled = false

      },
    }
  }
</script>

<style scoped>

</style>
```

配置页面路由  vuedev/src/router/index.js

```typescript
import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  routes: [
     {path: '/', redirect: '/index'},
    {
      path: '/index',
      name: 'index',
      component: () => import('../plugin/com/github/luanhy/sysinfo/web/index'),
    },
  ]
})
```

###### 6.4 插件结构

完成后插件包整体目录示例如下：

![输入图片说明](https://images.gitee.com/uploads/images/2020/0110/093308_c91c0bc0_1009390.png "插件目录.png")



##### 7 开发模式启动脚手架运行示例程序

至此，一个简单点的获取mac地址和cpu序列号的插件就完成了。

**启动 app.py 时增加参数 -p=dev** 

**表示开发环境 程序将一并启动前端dev环境，启动速度稍慢，显示调试页面**

启动中如图：

![输入图片说明](https://images.gitee.com/uploads/images/2020/0110/103359_543fc3b3_1009390.png "加载中.png")

启动完毕显示插件调式页面：

![输入图片说明](https://images.gitee.com/uploads/images/2020/0110/103202_70fa560d_1009390.png "加载完毕.png")



点击获取mac地址按钮和获取CPU序列号可以调用后端接口获取到信息

![输入图片说明](https://images.gitee.com/uploads/images/2020/0110/103321_e7fba073_1009390.png "获取信息.png")

##### 8 插件打包

点击 `开始-构建插件` 开始插件打包

片刻后弹出构建成功对话框

![输入图片说明](https://images.gitee.com/uploads/images/2020/0110/103601_de8f3307_1009390.png "构建插件成功.png")

点击`打开插件目录`可以找到构建好的插件文件

![输入图片说明](https://images.gitee.com/uploads/images/2020/0110/103900_a7323b16_1009390.png "打开插件目录.png")

##### 9 插件安装

上一步的插件打包后可以分享给其他用户安装，

点击 `开始-安装插件`，选择`上传插件包`， 选择上一步的插件包文件

![输入图片说明](https://images.gitee.com/uploads/images/2020/0110/104359_3d2ed808_1009390.png "安装插件.png")

片刻后显示插件安装完成

![输入图片说明](https://images.gitee.com/uploads/images/2020/0110/104506_40072992_1009390.png "插件安装完成.png")

点击重新加载  点击 `我的插件-系统工具-系统信息获取工具`菜单即可预览插件效果。

##### 10 正常模式启动脚手架运行示例程序

启动参数 -p=dev 去除后运行app.py即可 ，程序加载快，不启动前端环境，只显示已安装的插件。



##### 11 传送门

脚手架： [https://gitee.com/luanhaoyu_admin/py-web-dev-tools](https://gitee.com/luanhaoyu_admin/py-web-dev-tools)

示例项目：[https://gitee.com/luanhaoyu_admin/plugin_sys_info](https://gitee.com/luanhaoyu_admin/plugin_sys_info)

### 已集成工具

后续将补充一个插件仓库站，提供平台供插件开发者分享插件

1. pc设备 mac地址获取 cpu序列号获取

### 待集成工具

1. windows注册表管理
2. windows开机启动项管理
3. ...



### 联系作者

QQ：250985725

邮箱： 15951963820@163.com

博客地址：[https://blog.csdn.net/v2sking](https://blog.csdn.net/v2sking)

