from fastapi import FastAPI, Path
# import asyncio
import httpx

from app.models.input import Input
from app.models.response import Company
from app.config import third_party_apis
import json

app = FastAPI()


def validate_input(jurisdiction_code, company_number):
    return Input(
        jurisdiction_code=jurisdiction_code.lower(),
        company_number=company_number
    )


def log_request(input):
    # write to log stream
    pass


def get_api_list(input):
    return [i(input=input) for i in third_party_apis if input.jurisdiction_code in i.SUPPORTED_JURISDICTIONS]


def get_from_cache(api):
    return None


def call_api(api):
    response = httpx.get(api.endpoint)
    return json.loads(response.text)


def call_third_party(third_party_api):
    cached_result = get_from_cache(api=third_party_api)
    if cached_result:
        third_party_api.parse_response(cached_result)
    else:
        third_party_api.parse_response(call_api(third_party_api))


def merge_two_dicts(a: dict, b: dict):
    # modifies a with keys and values of b
    # but only if the value is a truthy
    # Note: this will fail with False 
    a.update({key: value for key, value in b.items() if value})


def filter_empty_data(item):
    if type(item) == dict:
        result = {}
        for key, value in item.items():
            if value is not None:
                result[key] = filter_empty_data(value)
        return result
    elif type(item) == list:
        result = []
        for i in item:
            result.append(filter_empty_data(i))
        return result
    elif type(item) is not None:
        return item
    
    

def create_response(api_list, input):
    if len(api_list) > 1:
        results = {}
        for i in [a.response_object.dict() for a in api_list[::-1] if a.response_object]:
            merge_two_dicts(results, i)
        return Company(**filter_empty_data(results))
    elif len(api_list) == 1:
        return Company(**filter_empty_data(api_list[0].response_object.dict()))
    else:
        return input


def log_response(response):
    pass


def process_request(jurisdiction_code, company_number):

    input = validate_input(jurisdiction_code=jurisdiction_code, company_number=company_number)
    api_list = get_api_list(input)
    for api in api_list:
        call_third_party(api)
    response = create_response(api_list=api_list, input=input)
    log_response(response)
    return response

# async def request(client):
#     response = await client.get(URL)
#     return response.text


# async def task():
#     async with httpx.AsyncClient() as client:
#         tasks = [request(client) for i in range(100)]
#         result = await asyncio.gather(*tasks)
#         print(result)



@app.get("/v1/company/{jurisdiction_code}/{company_number}", response_model=Company | Input, response_model_exclude_unset=True)
def get_company_info(
    jurisdiction_code: str = Path(
        regex="^[a-zA-Z]{2}$",
        min_length=2,
        max_length=2,
        title="Jurisdiction code",
        description="The 2 digit jurisdiction code where the company is registered",
        example="uk"
    ),
    company_number: str = Path(
        regex="^[a-zA-Z0-9]+$",
        min_length=1,
        max_length=4,
        title="Company number",
        description="The registration number for the company",
        example="1111"
    )
):
    return process_request(jurisdiction_code, company_number)
