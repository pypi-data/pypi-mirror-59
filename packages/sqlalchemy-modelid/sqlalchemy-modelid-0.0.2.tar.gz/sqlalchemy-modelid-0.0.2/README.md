# SQLAlchemy-ModelId

SQAlchemy-ModelId defines a base with a `model_id` property for [SQLAlchemy](https://www.sqlalchemy.org/) models.

The `model_id` property distinguishes model instances with the same identity from different tables.

## Example

After setup, we can access the `model_id` property as follows:

```python
my_model = Model()
session.add(my_model)
session.commit()
print(my_model.model_id)
```

Output:

```
model-1
```

## Documentation

You can find the latest documentation at [https://dsbowen.github.io/sqlalchemy-modelid](https://dsbowen.github.io/sqlalchemy-modelid).

## License

This project is licensed under the MIT License [LICENSE](https://github.com/dsbowen/sqlalchemy-modelid/blob/master/LICENSE).