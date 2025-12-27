# Observabilité d’un système de machine learning : j’avais tort depuis le début

Pendant longtemps, j’ai intégré les briques de machine learning comme des éléments à part entière des systèmes que je développais, en ajoutant parfois davantage de logs et de métriques afin de m’assurer que leur comportement respectait une certaine norme. Cela consistait notamment à définir des heuristiques ou des règles métier pour faire remonter des comportements jugés étranges du modèle et tenter de les observer.

Avec le recul, je pense que c’était une erreur fondamentale.

---

## Le modèle : un utilisateur comme un autre

> Le modèle n’est pas le système.
> - il n’est pas déterministe
> - il n’a pas d’invariants métier
> - il ne viole aucune règle explicite lorsqu’il se trompe
> - il ne peut pas être “buggé” au sens logiciel.

> Le modèle est un utilisateur du système.
> - Il consomme des entrées.
> - Il produit des propositions.  

Exactement comme un humain, une API externe ou un service tiers.

On n’observe pas un utilisateur.
On observe **ce que le système fait avec ses actions**.

---

## L’erreur silencieuse n’est pas un problème de modèle

L’**erreur silencieuse** correspond à une action du modèle sur le système qui ne garantit pas une qualité optimale du service rendu, sans pour autant produire d’erreur technique ou de signal explicite.

Dans de nombreux cas, le système délègue volontairement une décision au modèle, en acceptant une part d’incertitude. Lorsque la tâche à accomplir ne peut pas être exprimée de manière déterministe — compréhension du langage, classification sémantique, analyse contextuelle — le modèle est souvent la meilleure, voire la seule, solution possible.

Pendant longtemps, j’ai cherché à intégrer des garde-fous déterministes dans le code afin d’encadrer le modèle et de faire remonter des alertes. Mais il faut bien comprendre que toute la théorie du machine learning a précisément été développée parce que ces règles étaient trop restrictives. Aucune règle explicite ne saurait remplacer un modèle suffisamment robuste pour être utilisé en production.

L’erreur silencieuse n’est donc pas quelque chose que l’observabilité doit chercher à éliminer.
C’est une propriété intrinsèque des systèmes de machine learning.

---

## Mais alors, comment l’observabilité peut-elle nous assurer la qualité du service rendu ?

Elle ne le peut pas. Et elle ne doit pas prétendre le faire.

L’erreur est inhérente au machine learning. Elle fait partie du compromis accepté dès lors que l’on confie une tâche non déterministe à un modèle statistique. C’est précisément pour cette raison qu’il est plus sain de considérer le modèle comme un agent externe au système, et d’assumer explicitement le risque que cela implique.

Certains modèles sont toutefois capables de produire, en plus d’une prédiction, des signaux statistiques : score de confiance, estimation d’incertitude, probabilité associée à une classe. Ces informations peuvent être utiles, non pas pour juger la qualité intrinsèque de la prédiction, mais pour qualifier le contexte dans lequel elle est produite.

Utilisées correctement, ces notions d’incertitude ne servent pas à détecter automatiquement les “mauvaises” prédictions. Elles permettent au système de savoir qu’il agit dans une zone de doute, et d’en assumer les conséquences : accepter le risque, déclencher une revue humaine, ou simplement tracer cette incertitude comme une information métier.

L’observabilité ne permet donc pas de corriger les prédictions a posteriori, ni de retrouver de manière fiable celles qui seraient erronées. Chercher à l’utiliser dans ce but serait une confusion de rôles.

Ce qu’elle permet, en revanche, c’est de rendre visible l’impact métier réel des décisions prises à partir des prédictions du modèle : effets sur les utilisateurs, sur les flux, sur les délais, sur les coûts ou sur les indicateurs clés du service rendu.

L’identification fine des erreurs de prédiction, leur qualification et leur correction relèvent d’une autre brique du système : celle de l’annotation et du retour humain.
C’est cette boucle de feedback, volontairement séparée de l’observabilité, qui permet d’améliorer le modèle dans le temps.

L’observabilité n’améliore pas la qualité intrinsèque des prédictions.
Elle permet simplement de ne jamais perdre de vue leurs conséquences — et le niveau d’incertitude avec lequel elles ont été acceptées.

---

## Conclusion

J’ai longtemps cherché à rendre les modèles observables.  
Je pense aujourd’hui que c’était la mauvaise bataille.

L’observabilité d’un système de machine learning ne consiste pas à comprendre ce que fait le modèle, mais à **rendre explicite la manière dont ses sorties sont utilisées**.

Le modèle propose.  
Le système dispose.  
Et l’observabilité ne doit porter que sur ce qui est explicite, déterministe et responsable.
