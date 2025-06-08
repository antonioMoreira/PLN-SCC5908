# On deploy

```bash
python3.11 -m venv pln
source pln/bin/activate

pip install --upgrade pip setuptools wheel
pip install .

export LD_LIBRARY_PATH=/usr/src/app/pln/lib/python3.11/site-packages/nvidia/cudnn/lib/

uvicorn pln_api.app:app --port 5678 --host 0.0.0.0 --reload

```