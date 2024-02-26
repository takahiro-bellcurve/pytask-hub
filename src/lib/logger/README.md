
### `get_logger()`
`get_logger`でloggerクラスを呼び出し任意のログ出力に使用する。

使用例
```
from src.lib.logger import get_logger
logger = get_logger()

logger.info("xyz")
```
> [2024-02-09 15:23:32,670] INFO	logger.py:10 - main -> xyz

### `with_logging()`
デコレータ用の関数でデコレータした関数の開始と終了時、例外発生時を標準出力に出力するための関数

```
from src.lib.logger import get_logger, with_logging

logger = get_logger()

@with_logging(logger)
def test_function():
    print("xyz")
```
> [2024-02-09 15:23:32,670] INFO Users/your_user_name/dev/isaiah/tmp/test/logger.py:10 - test_function -> [START] test_function
xyz
[2024-02-09 15:23:32,670] INFO	Users/your_user_name/dev/isaiah/tmp/test/logger.py:10 - test_function -> [END] test_function
