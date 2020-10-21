# return self, return itself, return this, type self
from __future__ import annotations

class Example:
  @staticmethod
  def build() -> Example:
    return Example()
