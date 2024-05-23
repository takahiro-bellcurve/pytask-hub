import logging


class Logger:
    def __init__(self, name=__name__, level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # ログのフォーマットを設定
        formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s',
                                      datefmt='%Y/%d/%m %I:%M:%S')

        # コンソール出力用のハンドラを作成し、フォーマットを設定
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # ロガーにハンドラを追加
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger
