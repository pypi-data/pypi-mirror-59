# Line Extractor

Line Extractor is a Python CLI for extracting certain lines from text files given specified rules.

## Why you should use this CLI tool

If you're trying to read through thousands of lines of logs or just want to see every time the word "Donkey" shows up in the Shrek movie script this tool can help you do that. Instead of greping with regex you can use a more intutive CLI.

I created this tool because I got tired of reading through EC2 logs finding the lines beginning with certain phrases or ending with other phrases. So if this tool helps you out feel free to let me know!

## Installation

Use the package manager [pip](https://pypi.org/project/pip/) to install Line Extractor.

```bash
pip install lineExtractor
```

## Usage

General Format

```bash
lineExtractor [Options] source_file destination_file
```

Open the help menu

```bash
lineExtractor -h
```

Get all lines that contain the word "bee" and put them into output.txt

```bash
lineExtractor -c bee beeMovie.txt output.txt
```

Get all lines that start with "Hello" regardless of casing and put them into hello.txt

```bash
lineExtractor -b Hello -i speech.txt hello.txt
```

## Contributing

[Github](https://github.com/kvanland/lineExtractor/)

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Author

[Kyle Van Landingham](https://kvanland.github.io/)

## License

[MIT](https://choosealicense.com/licenses/mit/)