# Python Metrecord SDK

This package is the Python integration for metric tracking powered by [Metrecord](https://app.metrecord.com)

## Examples

Here are a couple examples you can use to get started:



```
from metrecord import Metrecord


recorder = Metrecord('CLIENT_ID', 'CLIENT_SECRET')
recorder.track('runtime_ms', 20.21)

```
