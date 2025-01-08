## Requirements
- Python 多分 >= 3.12 （うっかり [`type` statement](https://docs.python.org/3/library/typing.html#type-aliases) とかを使ったため．ちょっと直せば古いのでも動くと思われる）
- pandas  (2.2)
- numpy (2.2)
- plotly (5.24)

`pyproject.toml` があるのでそれを適宜参照

## Usage

- `*.tsv` を`data/` に置いておく
- `$ python main.py plot_by_emotion`: Emotion ごとにプロットして（ブラウザが開く），閲覧
	* wsl で動かす場合は，wsl から開けるブラウザがあることが必要 (`apt install firefox` が簡単ではある)．
- `$ python main.py print`: 読み取ったデータをそのまま標準出力に流す（もっぱら動作確認用）

## Options
- `--dir`: データを読み取るディレクトリを指定（デフォルトでは `data/`）
- `--filter-ref` など一部，条件でフィルタをかけられる．例えば `$ python main.py --filter-ref Self plot_by_emotion`
- `--filter-emo` は存在するが，現状表情ごとのプロットしかしないので無意味
