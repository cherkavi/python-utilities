# return self, return itself, return this, type self, type itself, generic 
from __future__ import annotations

class Example:
  @staticmethod
  def build() -> Example:
    return Example()
