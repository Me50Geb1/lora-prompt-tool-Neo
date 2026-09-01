# Forge Neo compatibility build

Version: 1.0.0-neo-compat1

Changes:
- Forge Neo / Gradio 4 compatibility for `gr.Box`.
- Forge Neo `models/embeddings` default path.
- Safe handling of removed/renamed command-line path attributes.
- Support for Neo `--ckpt-dirs` and `--lora-dirs` when resolving model files.
- Model metadata is resolved across configured model directories.
- User trigger-word edits are saved to `.json` and no longer overwrite Civitai Helper `.civitai.info` metadata.
- More robust localization directory lookup.

- compat2-red: Civitai model pages and API endpoints changed from civitai.com to civitai.red.
