from fastapi import Depends

def http_endpoint(read_request, create_use_case, create_answer):
    async def endpoint(request = Depends(read_request), use_case = Depends(create_use_case)):
        response = await use_case(request)
        http_answer = create_answer(response)
        return http_answer
    
    return endpoint