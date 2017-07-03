# Triple Selector Experiments

### Setup

* Install Python 2.7.x or later and `pip` (usually included)
* Install Python dependencies: `pip install -r scripts/requirements.txt`

### Running Experiments

Models comparison:

```
python classifier.py --mode compare_models triple-selector.train.csv
```

Feature sets comparison:

```
python classifier.py --mode compare_models triple-selector.train.csv
```

Train best model (Random Forest)

```
python classifier.py triple-selector.train.csv
```

OR

```
python classifier.py --mode train_models triple-selector.train.csv
```
