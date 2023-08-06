dnspod-sdk
===============

A dnspod api SDK.

`官方API文档 <https://www.dnspod.cn/docs/index.html>`_

安装
-------

.. code-block:: sh

    pip install dnspod-sdk

使用
-------

.. code-block:: py

    from dnspod_sdk import DnspodClient

    token_id = 0
    token = "<your token>"
    user_agent = "程序英文名称/版本(联系邮箱))"

    dc = DnspodClient(token_id, token, user_agent)

    r = dc.post("/Info.Version")
    print(r.json())

    r = dc.post("/Domain.List", data={"type": "all", "length": 1})
    print(r.json())
