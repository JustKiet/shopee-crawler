from langchain_core.pydantic_v1 import BaseModel, Field

# General Product Information JSON Structure
class ProductInfo(BaseModel):
    name: str = Field(description="Name of the product")
    discountedPrice: int = Field(description="Price of the product")
    discount: int = Field(description="Discount percentage of the product (INT ONLY, NO SYMBOLS)")
    salesCount: int = Field(description="Quantity sold of the product")

# Detailed Product Information JSON Structure
class DetailedProductInfo(BaseModel):
    manufacturerName: str = Field(description="Name of the manufacturer (BRAND)")
    intendedUse: str = Field(description="Intended use of the product")
    description: str = Field(description="Description (SHORTENED/SUMMARIZED) of the product")
    additionalInfo: str = Field(description="Additional (SHORTENED/SUMMARIZED) information about the product")