## Create Version

- Update version in `setup.cfg`
- Run following commands

```
python -m build
python -m twine upload dist/aputil-x.x.x* --config-file ./.pypirc
```