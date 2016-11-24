#!/usr/bin/env python
# -*- coding: utf-8 -*-
class Tweet:

    def __init__(self, id, tokens, original, classe, emojis):
        self.id = id
        self.tokens = tokens
        self.listaDeTokens = tokens.split();
        self.original = original
        self.classe = classe
        self.emojis = emojis