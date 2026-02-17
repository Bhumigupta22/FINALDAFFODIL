import sys
sys.path.insert(0, '/app')

from app.nlp_processor import NLPProcessor

def test_extract_command_add():
    nlp = NLPProcessor()
    assert nlp.extract_command("Add milk") == "add"
    assert nlp.extract_command("Buy apples") == "add"
    assert nlp.extract_command("I need bread") == "add"

def test_extract_command_remove():
    nlp = NLPProcessor()
    assert nlp.extract_command("Remove milk") == "remove"
    assert nlp.extract_command("Delete apples") == "remove"

def test_extract_category():
    nlp = NLPProcessor()
    assert nlp.extract_category("milk") == "dairy"
    assert nlp.extract_category("apple") == "produce"
    assert nlp.extract_category("cheese") == "dairy"

def test_extract_quantity():
    nlp = NLPProcessor()
    qty, unit = nlp.extract_quantity("Add 2 bottles of water")
    assert qty == 2.0
    assert unit == "bottle"
    
    qty, unit = nlp.extract_quantity("Add milk")
    assert qty == 1
    assert unit == ""

def test_process_voice_command():
    nlp = NLPProcessor()
    result = nlp.process_voice_command("Add two liters of milk")
    
    assert result["command"] == "add"
    assert "milk" in result["item_name"].lower()
    assert result["quantity"] == 2.0
    assert result["category"] == "dairy"

def test_empty_command():
    nlp = NLPProcessor()
    result = nlp.process_voice_command("")
    assert "error" in result

if __name__ == "__main__":
    test_extract_command_add()
    test_extract_command_remove()
    test_extract_category()
    test_extract_quantity()
    test_process_voice_command()
    test_empty_command()
    print("All NLP tests passed!")
