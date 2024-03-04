from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

member_lists = {
    1:{
        "name": "Monnana",
        "job": "Chef",
        "hobby": "chat with friends" 
    }
}

class Member(BaseModel):
    name: str
    job: str
    hobby: str

class UpdateMember(BaseModel):
    name: Optional[str] = None
    job: Optional[str] = None
    hobby: Optional[str] = None

@app.get("/")
def index():
    return {"name": "first data"}

@app.get("/get-member/{member_id}", tags=['member'], description='The ID of the member u wanna know')
def get_member(member_id: Optional[int] = None):
    try:
        return member_lists[member_id]
    except:
        return f"There is no {member_id} member here!"

@app.get("/get-member-name", tags=['member'], description="Show whether the member name is in our list")  
def get_name(member_name: str):
    for member_value in member_lists.values():
        if member_name==member_value['name']:
            return member_value
    return f"There is no {member_name} here!"

# create new data
@app.post("/create-member/{member_id}", tags=['member'], description="Create new member by input.")
def create_member(member_id: int, member: Member):
    if member_id in member_lists:
        return {"Error": "Member exists."}
    
    member_lists[member_id] = member
    return member_lists[member_id]

# update existed data
@app.put("/update-member/{member_id}", tags=['member'], description="Update member information by input.")
def update_member(member_id: int, member: UpdateMember):
    if member_id not in member_lists:
        return {"Error": "Member doesn't exist."}
    
    #member_lists[member_id] = member

    if member.name != None:
        member_lists[member_id].name = member.name

    if member.job != None:
        member_lists[member_id].job = member.job

    if member.hobby != None:
        member_lists[member_id].hobby = member.hobby

    return member_lists[member_id]

# delete existed data
@app.delete("delete-member/{member_id}")
def delete_member(member_id: int):
    if member_id not in member_lists:
        return {"Error": "Member doesn't exist."}
    
    del member_lists[member_id]
    return {"Message": "Member deleted successfully."}

## terminal command
# cd to the fastapi python code directory
# uvicorn [python file]:[FastAPI object] --reload
# ex: uvicorn FastAPI:app --reload

# default local url: http://127.0.0.1:8000
# url for api management: http://127.0.0.1:8000/docs