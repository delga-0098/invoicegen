import json

from invoicegen.models import Invoice

schema = Invoice.model_json_schema()
print(json.dumps(schema, indent=2))
