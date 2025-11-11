import json

from invoicegen.models_header import InvoiceHeader

schema = InvoiceHeader.model_json_schema()
print(json.dumps(schema, indent=2))
