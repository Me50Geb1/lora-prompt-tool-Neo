# LoRA Prompt Tool Neo

> [!NOTE]
> This is an unofficial Forge Neo compatibility fork of
> [a2569875/lora-prompt-tool](https://github.com/a2569875/lora-prompt-tool).
>
> This fork is not maintained by the original author.

**sd-webui-forge-neo** 向けに互換性修正を加えた LoRA Prompt Tool です。

元の LoRA Prompt Tool の機能を維持しながら、Forge Neo で動作するように修正しています。

## Forge Neo Changes

- sd-webui-forge-neo のモデルディレクトリ構成に対応
- 複数のLoRAモデルディレクトリに対応
- Forge Neo / Gradio環境向けのUI互換性修正
- Civitai Helperとの併用を考慮したメタデータ処理
- `.json` と `.civitai.info` の競合を回避
- Civitai関連URLの `civitai.red` 対応
- Forge Neo環境でのLoRA情報取得処理を調整
- Extra Networksとの互換性を考慮した処理

## Installation

Forge Neo の `extensions` フォルダ内でCloneします。

    git clone -b forge-neo https://github.com/Me50Geb1/lora-prompt-tool-Neo.git

配置例:

    sd-webui-forge-neo/
    └─ extensions/
       └─ lora-prompt-tool-Neo/

インストール後、Forge Neoを再起動してください。

## Important

このForkでは主に **Forge Neoとの互換性維持** を目的としています。

元プロジェクトとは別の非公式Forkです。

不具合を元作者へ報告する場合、このFork固有の問題でないことを確認してください。

## Support Notice

This Forge Neo compatibility version was modified with the assistance of ChatGPT.

The repository owner may not be able to answer technical questions, provide support, or respond to implementation-related inquiries.

このForge Neo対応版はChatGPTの支援により修正されています。

リポジトリ所有者は技術的な質問、サポート、実装に関する問い合わせには対応できない場合があります。

## Neo Compatibility Notes

See [NEO_COMPAT.md](NEO_COMPAT.md).

---

# Original README

[![Python](https://img.shields.io/badge/Python-%E2%89%A73.10-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/github/license/a2569875/lora-prompt-tool)](https://github.com/a2569875/lora-prompt-tool/blob/main/LICENSE)
# LoRA Model Prompt Tool

When you have trained many LoRA models, each model usually has its own model prompt, trigger words and usage method. In the past, external tools were needed to record them. This extension can help you save these model prompts and dedicated prompts, and quickly call them up when needed.

[![buy me a coffee](readme/Artboard.svg)](https://www.buymeacoffee.com/a2569875 "buy me a coffee")

[![LoRA-Prompt-Tool](https://res.cloudinary.com/marcomontalbano/image/upload/v1687840465/video_to_markdown/images/youtube--MVUNoxjrCzE-c05b58ac6eb4c4700831b2b3070cd403.jpg)](https://youtu.be/MVUNoxjrCzE "LoRA-Prompt-Tool")

# Installation

Go to \[Extensions\] -> \[Install from URL\] in webui and enter the following URL:
```
https://github.com/a2569875/lora-prompt-tool.git
```
Install and restart to complete installation.

# Features

* 1. Automatic add trigger words to prompts
  - Insert prompts at the end of the prompt input box
  - Insert prompts at the position where there are double commas ",,"
  - Divided into prompts and reverse prompts
  - Support txt2img and img2img

* 2. Prompt search/filtering: When there are many prompts for a particular model, you can search/filter the prompts
  - Supports regex search

* 3. Editing and managing prompts
  - Dedicated tab for editing prompts
  - Can add, modify, delete prompts
  - Supports CivitAI's JSON format
  - Delete duplicate prompts
  - Sort prompts
  - Translate prompts

* 4. Batch import of prompts
  - Import from Civitai
  - Import from Dreambooth models
  - Import multiple lines of text

  ## Videos
[![LoRA-Prompt-Tool!](https://res.cloudinary.com/marcomontalbano/image/upload/v1683644210/video_to_markdown/images/youtube--QQ9YVjCO_9s-c05b58ac6eb4c4700831b2b3070cd403.jpg)](https://www.youtube.com/watch?v=QQ9YVjCO_9s "LoRA-Prompt-Tool!")
  
  ## Acknowledgements
*  [JackEllie's Stable-Siffusion community team](https://discord.gg/TM5d89YNwA) 、 [Youtube channel](https://www.youtube.com/@JackEllie)
*  [Chinese Wikipedia community team](https://discord.gg/77n7vnu)

<p align="center"><img src="https://count.getloli.com/get/@sd-webui-lora-prompt-tool.github" alt="sd-webui-lora-prompt-tool"></p>
