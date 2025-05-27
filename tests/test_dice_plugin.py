import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'bot')))
import asyncio
from plugins.dice import DicePlugin

async def run_execute():
    plugin = DicePlugin()
    result = await plugin.execute('send_dice', None)
    return result

def test_dice_execute():
    result = asyncio.run(run_execute())
    assert result['direct_result']['kind'] == 'dice'
    assert result['direct_result']['format'] == 'dice'
    assert result['direct_result']['value'] == '🎲'


def test_dice_spec():
    plugin = DicePlugin()
    specs = plugin.get_spec()
    assert isinstance(specs, list)
    assert specs[0]['name'] == 'send_dice'
