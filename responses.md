# Réponses

## Exercice 1:
1. Une route GET /stations crée une station. Quel verbe et quel code HTTP faut-il utiliser pour cette création ?
-> "POST /stations" qui rend 201

2. GET /stations/999 demande une station inexistante. Quel code HTTP et quel type de réponse faut-il renvoyer ?
-> 404

3. Quelle est la différence entre les codes 401 et 403 ? Donnez un exemple de chaque cas.
-> Le code 401 veut dire "Non autorisé" (Unauthorized), il apparaît quand l'utilisateur n'est pas authentifié ou que ses identifiants sont faux, à l'inverse, le code 403 veut dire qu'il est bien authentifié mais qu'il n'a pas les droits nécessaires (Forbidden).
Ex 401: accéder à un pannel administrateur sans être connecté.
Ex 403: accéder au pannel administrateur en étant un simple "user".

## Exercice 3:
Code 200:
{
  "id": 1,
  "code": "ST-001",
  "name": "test",
  "capacity": 10,
  "status": "open"
}

## Exercice 4:
Premier test : python -m pytest -q
8 passed, 1 warning in 0.08s (le warning est causé par un package deprecated)

Deuxième test : python -m pytest -q
8 passed, 1 warning in 0.08s (le warning est causé par un package deprecated)