up2smms
========

这是基于 `picbed <https://github.com/staugur/picbed>`_
的一个小的扩展模块，用来将上传的图片保存到
`sm.ms公共图床 <https://sm.ms>`_

安装
------

- 正式版本

    `$ pip install -U up2smms`

- 开发版本

    `$ pip install -U git+https://github.com/staugur/picbed-up2smms.git@master`

开始使用
----------

此扩展请在部署 `picbed <https://github.com/staugur/picbed>`_ 图床后使用，需要
其管理员进行添加扩展、设置钩子等操作。

添加：
^^^^^^^^

请在 **站点管理-钩子扩展** 中添加第三方钩子，输入名称：up2smms，
确认后提交即可加载这个模块（请先手动安装好此模块）。

配置：
^^^^^^^^

在 **站点管理-网站设置** 底部的钩子配置区域配置sm.ms的API Secret Token，
若不配置，那么则会匿名上传sm.ms！

使用：
^^^^^^^^

同样在 **站点管理-网站设置** 上传区域中选择存储后端为up2smms即可，
后续图片上传时将保存到sm.ms！
