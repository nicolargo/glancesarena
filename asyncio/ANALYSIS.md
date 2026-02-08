# Analyse du code asyncio/ — Recommandations

## 1. L'async n'est pas réellement async (P0)

`plugin.update()` est synchrone et bloquant. Les appels psutil bloquent l'event loop.
`asyncio.gather()` ne parallélise rien car chaque coroutine bloque pendant l'appel psutil.
`asyncio.run()` dans le while loop recrée l'event loop à chaque itération.

**Recommandation :** Utiliser `asyncio.to_thread()` pour les appels psutil et garder un event loop persistant.

## 2. Le polymorphisme de `_stats` (dict | list | None) (P0)

Chaque méthode de transformation doit tester les 3 cas avec `isinstance()`.
Le bug de merge par index (documenté lignes 184-208) en est la conséquence directe.

**Recommandation :** Unifier sur `dict[str, dict]` avec clé sentinelle pour les plugins sans clé.

## 3. Violation SRP — GlancesPlugin fait trop de choses (P1)

490 lignes mélangeant collecte, transformation, métadonnées et rendu.

**Recommandation :** Séparer en Collector / Transformer / Renderer.

## 4. Deux architectures divergentes asyncio/ vs stats/ (P1)

Deux systèmes parallèles pour le rate calculation, l'historique et les plugins keyés.

**Recommandation :** Converger. Le modèle `Stat` de stats/ est bon, l'intégrer dans la base async.

## 5. Structures non typées (P1)

`_object` est un "god dict" non typé. `stats_def` est mutable et modifié de manière impérative.

**Recommandation :** Utiliser des dataclass/Pydantic pour PluginResult et stats_def.

## 6. Pas de découverte automatique des plugins (P2)

Imports manuels + `sys.modules` pour la découverte.

**Recommandation :** Registre via décorateur ou introspection automatique du package.

## 7. Singletons module-level (P2)

Empêchent le testing, la configuration dynamique et la gestion du cycle de vie.

**Recommandation :** Factory ou conteneur d'injection.

## 8. Qualité (P2)

- `raise("string")` ne lève aucune exception (plugin.py:158)
- `print()` au lieu de `logging`
- Pas de type hints dans plugin.py
- Syntaxe Python 2 (`GlancesPlugin(object)`, `super(Cpu, self)`)
- `get` property expose l'état interne mutable
- Zéro test

## Priorités

| Priorité | Sujet |
|----------|-------|
| P0 | Rendre l'async réellement async |
| P0 | Unifier `_stats` sur `dict[str, dict]` |
| P1 | Séparer collecte / transformation / rendu |
| P1 | Converger asyncio/ et stats/ |
| P1 | Typer les structures |
| P2 | Registre de plugins + suppression singletons |
| P2 | Logging, tests, syntaxe Python 3 moderne |
