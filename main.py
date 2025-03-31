import sys
import yaml

from GalTransl.__main__ import worker
from pathlib import Path

galtransl_dir = Path(__file__).parent.resolve()
project_dir = galtransl_dir / "sampleProject"


def edit_config():
    if len(sys.argv) < 4:
        exit(1)
    token, endpoint, rewrite_model_name = sys.argv[1:4]
    with open(project_dir / "config.inc.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    gpt4_config = config["backendSpecific"]["GPT4"]
    gpt4_config["tokens"][0]["token"] = token
    gpt4_config["tokens"][0]["endpoint"] = endpoint
    gpt4_config["rewriteModelName"] = rewrite_model_name
    config['common']['linebreakSymbol'] = '\\n'
    with open(project_dir / "config.inc.yaml", "w", encoding="utf-8") as f:
        yaml.dump(config, f, sort_keys=False, allow_unicode=True)


def main():
    input_path = project_dir / 'gt_input'
    if not input_path.exists() or not any(input_path.iterdir()):
        return
    
    edit_config()
    exit(worker(str(project_dir), "config.inc.yaml", "gpt4"))


if __name__ == "__main__":
    main()
