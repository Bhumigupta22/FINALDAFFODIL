import sys
sys.path.insert(0, '/app')

from app.database import add_shopping_item, get_shopping_list, remove_shopping_item

def test_add_item():
    item_id = add_shopping_item("Test Milk", "dairy", 1, "bottle")
    assert item_id is not None
    
    items = get_shopping_list()
    assert any(item['item_name'] == "Test Milk" for item in items)

def test_remove_item():
    item_id = add_shopping_item("Test Item", "other")
    remove_shopping_item(item_id)
    
    items = get_shopping_list()
    assert not any(item['id'] == item_id for item in items)

def test_get_empty_list():
    # Clear all items first
    items = get_shopping_list()
    for item in items:
        remove_shopping_item(item['id'])
    
    items = get_shopping_list()
    assert len(items) == 0

if __name__ == "__main__":
    test_add_item()
    test_remove_item()
    test_get_empty_list()
    print("All database tests passed!")
