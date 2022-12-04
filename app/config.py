from app.configs.third_party_a import ThirdPartyA
from app.configs.third_party_b import ThirdPartyB

# The order is important. We merge the result sets with 
# the highest priority given to those 1st in the list
third_party_apis = [
    ThirdPartyA,
    ThirdPartyB
]
