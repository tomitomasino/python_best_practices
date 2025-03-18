import sys
from pathlib import Path
import yaml
import jsonschema

# Define schema for business parameters
SCHEMA = {
    "type": "object",
    "required": ["pricing", "inventory", "notifications"],
    "properties": {
        "pricing": {
            "type": "object",
            "required": ["discount_tiers", "minimum_order"],
            "properties": {
                "discount_tiers": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["threshold", "percentage"],
                        "properties": {
                            "threshold": {"type": "number", "minimum": 0},
                            "percentage": {"type": "number", "minimum": 0, "maximum": 100}
                        }
                    }
                },
                "minimum_order": {"type": "number", "minimum": 0}
            }
        },
        "inventory": {
            "type": "object",
            "required": ["low_stock_threshold", "max_items_per_order"],
            "properties": {
                "low_stock_threshold": {"type": "number", "minimum": 0},
                "max_items_per_order": {"type": "number", "minimum": 1}
            }
        }
    }
}

def validate_params(env: str) -> bool:
    """Validates business parameters for given environment"""
    params_file = Path(__file__).parent.parent / "business_params" / f"{env}.yaml"
    
    if not params_file.exists():
        print(f"Error: No business parameters file for environment: {env}")
        return False
        
    with open(params_file) as f:
        params = yaml.safe_load(f)
        
    try:
        jsonschema.validate(instance=params, schema=SCHEMA)
        print(f"✓ Business parameters for {env} are valid")
        return True
    except jsonschema.exceptions.ValidationError as e:
        print(f"Error validating business parameters: {e.message}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_business_params.py <environment>")
        sys.exit(2)
        
    env = sys.argv[1]
    if not validate_params(env):
        sys.exit(1)
