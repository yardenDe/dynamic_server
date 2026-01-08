from pydantic import BaseModel

api_manager = None

class SelectQuery(BaseModel):
    table: str
    fields: list[str]

def setupRoutes(app):

    @app.post("/select")
    def select_fields(query: SelectQuery):
        table = query.table
        fields = query.fields
        return {"results": api_manager.manage_queries(table, fields=fields)}