import asyncio
import sys

from scripts.create_roles import create_roles
from scripts.reset_settings import reset_settings

SCRIPTS = [
    create_roles,
    reset_settings
]

if __name__ == "__main__":
    for i in range(len(SCRIPTS)):
        print(f"{i+1}. {SCRIPTS[i].__name__}")
    n = int(input("Select script: "))
    asyncio.run(SCRIPTS[n-1]())
