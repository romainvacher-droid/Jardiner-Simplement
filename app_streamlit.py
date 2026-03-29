#!/usr/bin/env python3
"""
🌱 Jardiner Simplement — Site web de conseils jardinage
Lancez avec : streamlit run app_streamlit.py
"""

import streamlit as st
from datetime import date
import random

st.set_page_config(
    page_title="Jardiner Simplement",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# DONNÉES JARDINAGE
# ─────────────────────────────────────────────────────────────────────────────

CONSEILS_DU_JOUR = [
    "Arrosez toujours au pied des plantes, jamais sur les feuilles pour éviter les maladies.",
    "Un paillis de 5 cm autour de vos plants économise jusqu'à 50% d'eau.",
    "Récoltez vos légumes le matin : ils sont plus gorgés de saveur.",
    "Les vers de terre sont vos meilleurs alliés — ne retournez pas inutilement la terre.",
    "Une poignée de marc de café au pied des tomates les aide à mieux fructifier.",
    "Associez basilic et tomates : le basilic repousse les pucerons et améliore le goût.",
    "Plantez la lune descendante pour les racines, montante pour les fruits et fleurs.",
    "Les feuilles de fougère en paillis repoussent les limaces naturellement.",
    "Taillez toujours avec des outils propres et tranchants pour éviter les maladies.",
    "Les orties en purée nourrissent et protègent — un engrais naturel incomparable.",
    "Semez des capucines autour du potager : elles attirent les pucerons loin de vos légumes.",
    "Un compost bien fait ne sent pas mauvais — ajoutez des matières sèches si ça sent.",
    "Arrosez le soir en été pour limiter l'évaporation.",
    "Laissez quelques herbes monter en graine : elles attireront les insectes auxiliaires.",
    "Cueillez les fleurs fanées régulièrement pour prolonger la floraison.",
    "Un sarclage après la pluie est bien plus efficile qu'en terre sèche.",
    "Les écorces de banane au pied des rosiers apportent du potassium.",
    "Associez carottes et oignons : ils se protègent mutuellement de leurs parasites.",
    "Les coquilles d'œufs broyées autour des semis découragent les limaces.",
    "Récupérez l'eau de cuisson des légumes (refroidie) pour arroser vos plantes.",
    "Un rang de soucis dans le potager protège toutes les cultures alentour.",
    "Pincez les gourmands de tomates pour concentrer l'énergie sur les fruits.",
    "Semez des engrais verts en automne pour nourrir et protéger le sol en hiver.",
    "Une bonne rotation des cultures sur 4 ans épuise les maladies spécifiques.",
    "Évitez de marcher sur la terre humide : vous détruisez sa structure.",
]

CALENDRIER = {
    1:  {
        "nom": "Janvier",
        "semis": ["Laitues (sous abri)", "Tomates (très tôt, sous serre chaude)", "Poivrons (sous serre)"],
        "planter": ["Arbres fruitiers à racines nues (si sol non gelé)", "Ail", "Échalotes"],
        "recolter": ["Choux de Bruxelles", "Poireaux", "Mâche", "Épinards d'hiver", "Kale"],
        "travaux": ["Tailler les arbres fruitiers (pommiers, poiriers)", "Préparer le compost", "Commander les semences", "Nettoyer et ranger les outils"],
        "conseil": "Le jardin se repose. Profitez-en pour planifier la saison et commander vos semences.",
    },
    2:  {
        "nom": "Février",
        "semis": ["Tomates (sous serre chaude)", "Poivrons", "Aubergines", "Salades (sous abri)", "Poireaux", "Oignons"],
        "planter": ["Ail", "Échalotes", "Pommes de terre primeurs (sous abri)", "Framboisiers"],
        "recolter": ["Mâche", "Épinards", "Poireaux", "Choux", "Bettes"],
        "travaux": ["Tailler les rosiers et petits fruits", "Préparer les bacs à semis", "Désherber à la houe par temps sec", "Pailler les fraisiers"],
        "conseil": "Les jours rallongent. Il est temps de préparer vos semis sous abri.",
    },
    3:  {
        "nom": "Mars",
        "semis": ["Tomates", "Courgettes (sous abri)", "Concombres (sous abri)", "Haricots (sous abri)", "Betteraves", "Radis", "Épinards", "Carottes (en place)"],
        "planter": ["Oignons", "Échalotes", "Pommes de terre (tôt)", "Petits pois", "Fraisiers"],
        "recolter": ["Épinards", "Mâche", "Oseille", "Rhubarbe (premières tiges)"],
        "travaux": ["Bêcher légèrement les massifs", "Nettoyer les allées", "Installer les tuteurs", "Préparer les buttes pour les courges"],
        "conseil": "La saison démarre ! Semez à l'abri et durcissez progressivement vos plants.",
    },
    4:  {
        "nom": "Avril",
        "semis": ["Courgettes", "Courges", "Haricots verts", "Maïs (sous abri)", "Basilic", "Tournesols", "Laitues", "Betteraves"],
        "planter": ["Pommes de terre", "Petits pois", "Oignons", "Poireaux (repiquage)", "Choux (plants)"],
        "recolter": ["Radis", "Oseille", "Asperges", "Épinards", "Rhubarbe", "Laitues d'hiver"],
        "travaux": ["Repiquer les tomates si temps doux (après Saints de Glace = avant mi-mai)", "Semer les engrais verts", "Pailler généreusement", "Installer le système d'arrosage"],
        "conseil": "Attention aux gelées tardives ! Protégez vos plants sensibles jusqu'aux Saints de Glace.",
    },
    5:  {
        "nom": "Mai",
        "semis": ["Haricots en place", "Courges en place", "Basilic en place", "Cornichons", "Navets"],
        "planter": ["Tomates (après le 15)", "Poivrons", "Aubergines", "Courgettes (plants)", "Melons (sous abri)"],
        "recolter": ["Asperges", "Radis", "Salades", "Petits pois (premiers)", "Fraises", "Rhubarbe"],
        "travaux": ["Pincer les gourmands des tomates", "Buter les pommes de terre", "Désherber régulièrement", "Installer les filets anti-insectes"],
        "conseil": "Après les Saints de Glace (11, 12, 13 mai), plus de risque de gel — plantez tout !",
    },
    6:  {
        "nom": "Juin",
        "semis": ["Haricots (2e semis)", "Carottes (2e semis)", "Laitues (résistantes chaleur)", "Fenouil", "Betteraves (2e semis)"],
        "planter": ["Poireaux d'automne", "Céleris-raves", "Brocolis d'automne"],
        "recolter": ["Fraises", "Petits pois", "Radis", "Salades", "Courgettes (premières)", "Cerises", "Ail nouveau"],
        "travaux": ["Arroser tôt le matin ou le soir", "Pailler pour retenir l'humidité", "Attacher les tomates", "Traiter préventivement contre le mildiou"],
        "conseil": "La chaleur arrive. Le paillage devient indispensable pour économiser l'eau.",
    },
    7:  {
        "nom": "Juillet",
        "semis": ["Navets", "Épinards (pour automne)", "Mâche", "Radis d'automne", "Laitues d'automne"],
        "planter": ["Choux d'automne et d'hiver", "Poireaux d'automne", "Céleri"],
        "recolter": ["Courgettes", "Haricots verts", "Tomates (premières)", "Concombres", "Pommes de terre nouvelles", "Oignons", "Framboises", "Myrtilles"],
        "travaux": ["Arroser régulièrement", "Récolter souvent pour stimuler la production", "Tailler les stolons des fraisiers", "Ébourgeonnage des tomates"],
        "conseil": "Récoltez souvent ! Un légume oublié arrête la production de la plante.",
    },
    8:  {
        "nom": "Août",
        "semis": ["Mâche", "Épinards", "Radis", "Navets", "Laitues résistantes", "Carottes (pour hiver)"],
        "planter": ["Choux de Bruxelles", "Brocolis tardifs", "Fraisiers (nouvelle plantation)"],
        "recolter": ["Tomates", "Poivrons", "Aubergines", "Courgettes", "Haricots verts", "Maïs", "Melons", "Prunes", "Pommes tôt"],
        "travaux": ["Préparer les planches pour les semis d'automne", "Faire les conserves", "Bouturer les géraniums", "Tailler les haies (dernière fois)"],
        "conseil": "C'est la pleine abondance ! Préparez déjà vos semis d'automne en fin de mois.",
    },
    9:  {
        "nom": "Septembre",
        "semis": ["Épinards", "Mâche", "Ail (plantation)", "Laitues d'hiver", "Bleuets et fleurs bisannuelles"],
        "planter": ["Ail d'automne", "Oignons blancs", "Fraisiers", "Bulbes de printemps (jacinthes, tulipes)"],
        "recolter": ["Tomates (avant premières gelées)", "Courges et citrouilles", "Pommes de terre", "Oignons", "Pommes", "Poires", "Raisins"],
        "travaux": ["Stocker les courges", "Ramasser les noix et noisettes", "Semer un engrais vert", "Préparer le potager pour l'hiver"],
        "conseil": "Récoltez les courges avant les gelées — elles se conservent 6 mois à l'abri.",
    },
    10: {
        "nom": "Octobre",
        "semis": ["Épinards résistants", "Blé ou phacélie (engrais vert)", "Pois (sous abri)"],
        "planter": ["Ail", "Tulipes", "Narcisses", "Jacinthes", "Arbres et arbustes"],
        "recolter": ["Dernières tomates", "Poireaux", "Poireaux", "Choux", "Betteraves", "Carottes", "Céleri", "Pommes tardives"],
        "travaux": ["Ramasser les feuilles mortes (compost ou paillis)", "Butter les poireaux", "Rentrer les plantes frileuses", "Tailler les touffes vivaces"],
        "conseil": "Plantez les bulbes maintenant pour de belles fleurs au printemps.",
    },
    11: {
        "nom": "Novembre",
        "semis": ["Pois (sous abri froid)", "Fèves (sous abri)"],
        "planter": ["Ail tardif", "Arbres fruitiers à racines nues (si sol non gelé)", "Haies"],
        "recolter": ["Poireaux", "Mâche", "Choux de Bruxelles", "Choux kale", "Topinambours", "Courges (conservation)"],
        "travaux": ["Rentrer les dernières plantes", "Protéger les cultures fragiles avec un voile", "Nettoyer le potager", "Pailler les vivaces"],
        "conseil": "Protégez la terre avec un paillis — un sol nu en hiver se dégrade et se perd.",
    },
    12: {
        "nom": "Décembre",
        "semis": [],
        "planter": ["Arbres à racines nues par temps doux"],
        "recolter": ["Choux de Bruxelles", "Poireaux", "Mâche", "Épinards d'hiver", "Topinambours"],
        "travaux": ["Tailler les arbres fruitiers", "Commander les semences", "Entretenir les outils", "Planifier la rotation des cultures"],
        "conseil": "Profitez du calme du jardin pour planifier et rêver à la prochaine saison.",
    },
}

LEGUMES = {
    "Tomate": {
        "emoji": "🍅",
        "description": "Reine du potager, la tomate est incontournable. Exigeante en soleil et chaleur, elle récompense généreusement le jardinier attentif.",
        "semis": "Février–mars (sous abri chaud)",
        "plantation": "Après le 15 mai (après les Saints de Glace)",
        "recolte": "Juillet–octobre",
        "exposition": "Plein soleil (minimum 6h/jour)",
        "arrosage": "Régulier, au pied — éviter les feuilles",
        "espacement": "60–80 cm entre les plants",
        "associations_positives": ["Basilic 🌿", "Persil", "Carottes", "Œillets d'Inde"],
        "associations_negatives": ["Fenouil", "Choux", "Pommes de terre"],
        "maladies": "Mildiou (taches brunes), alternariose",
        "conseil": "Pincez les gourmands (tiges secondaires à l'aisselle) pour concentrer l'énergie sur les fruits. Tuteurez dès la plantation.",
    },
    "Courgette": {
        "emoji": "🥒",
        "description": "Facile et productive, la courgette est idéale pour les débutants. Attention : une plante suffit pour une famille !",
        "semis": "Avril–mai (sous abri), mai en pleine terre",
        "plantation": "Mi-mai après les gelées",
        "recolte": "Juillet–octobre",
        "exposition": "Soleil, mi-ombre toléré",
        "arrosage": "Abondant, régulier",
        "espacement": "1 m entre les plants",
        "associations_positives": ["Haricots", "Maïs", "Capucines", "Oignons"],
        "associations_negatives": ["Fenouil", "Pommes de terre"],
        "maladies": "Oïdium (poudre blanche sur feuilles)",
        "conseil": "Récoltez les courgettes petites (15–20 cm) : elles sont plus savoureuses et la plante continue de produire.",
    },
    "Carotte": {
        "emoji": "🥕",
        "description": "La carotte demande un sol meuble et profond, sans cailloux. Elle se sème directement en place.",
        "semis": "Mars–juillet en place",
        "plantation": "Semis direct uniquement",
        "recolte": "Juillet–novembre selon variété",
        "exposition": "Soleil ou mi-ombre légère",
        "arrosage": "Modéré et régulier",
        "espacement": "Éclaircir à 5–8 cm",
        "associations_positives": ["Oignons", "Poireaux", "Tomates", "Sauge"],
        "associations_negatives": ["Fenouil", "Betteraves", "Aneth"],
        "maladies": "Mouche de la carotte (protéger avec filet)",
        "conseil": "Semez avec de la litière de chanvre ou du sable pour mieux répartir les graines. Couvrez d'un filet anti-insectes dès le semis.",
    },
    "Haricot vert": {
        "emoji": "🫘",
        "description": "Facile, productif et enrichissant le sol en azote. Idéal pour débuter.",
        "semis": "Mai–juillet en place (pas de repiquage)",
        "plantation": "Semis direct — il déteste être transplanté",
        "recolte": "Juillet–septembre",
        "exposition": "Plein soleil",
        "arrosage": "Régulier, surtout à la floraison",
        "espacement": "8–10 cm en rang, rangs à 40 cm",
        "associations_positives": ["Courgettes", "Maïs", "Concombres", "Carottes"],
        "associations_negatives": ["Oignons", "Poireaux", "Ail", "Fenouil"],
        "maladies": "Anthracnose (taches noires), araignées rouges par chaleur",
        "conseil": "Récoltez avant que les graines ne gonflent dans la cosse. Évitez de toucher les plants quand ils sont mouillés.",
    },
    "Salade": {
        "emoji": "🥬",
        "description": "Culture rapide et facile, la salade tolère la mi-ombre. Parfaite pour remplir les espaces entre autres cultures.",
        "semis": "Mars–septembre (toutes les 3 semaines pour étaler la récolte)",
        "plantation": "Repiquage à 4 feuilles",
        "recolte": "45–70 jours après semis selon variété",
        "exposition": "Soleil au printemps, mi-ombre en été",
        "arrosage": "Régulier, sans excès",
        "espacement": "25–30 cm",
        "associations_positives": ["Radis", "Carottes", "Fraisiers", "Concombres"],
        "associations_negatives": ["Céleri", "Persil"],
        "maladies": "Limaces, mildiou en excès d'humidité",
        "conseil": "Récoltez le matin, feuille par feuille sur les variétés à couper : la plante continue à pousser.",
    },
    "Pomme de terre": {
        "emoji": "🥔",
        "description": "Facile à cultiver, la pomme de terre s'adapte à presque tous les sols. Le buttage est essentiel.",
        "semis": "Plantation de plants (tubercules)",
        "plantation": "Mars–avril (primeurs), avril–mai (saison)",
        "recolte": "Juillet–octobre selon variété",
        "exposition": "Soleil",
        "arrosage": "Modéré, régulier",
        "espacement": "30–35 cm entre les plants, 70 cm entre les rangs",
        "associations_positives": ["Maïs", "Haricots", "Chou", "Persil"],
        "associations_negatives": ["Tomates", "Courges", "Tournesol", "Fenouil"],
        "maladies": "Mildiou, doryphore (coléoptère rayé jaune-noir)",
        "conseil": "Buttez 2–3 fois au cours de la saison. La récolte peut se faire quand les fanes jaunissent et tombent.",
    },
    "Poireau": {
        "emoji": "🧅",
        "description": "Le poireau est rustique et occupe le jardin l'automne et l'hiver quand peu de légumes sont disponibles.",
        "semis": "Janvier–avril (sous abri), mars en place",
        "plantation": "Repiquage de juin à août",
        "recolte": "Septembre–mars",
        "exposition": "Soleil ou mi-ombre",
        "arrosage": "Régulier",
        "espacement": "15–20 cm",
        "associations_positives": ["Carottes", "Céleris", "Tomates"],
        "associations_negatives": ["Haricots", "Pois"],
        "maladies": "Rouille du poireau (taches orange), mouche de l'oignon",
        "conseil": "Repliquer dans un trou profond (15 cm) en coupant feuilles et racines de moitié : le poireau s'étiolera et blanchira naturellement.",
    },
    "Courge": {
        "emoji": "🎃",
        "description": "Les courges et citrouilles sont très décoratives et conservent plusieurs mois. Elles nécessitent beaucoup d'espace.",
        "semis": "Avril–mai sous abri",
        "plantation": "Après le 15 mai, en butte enrichie",
        "recolte": "Septembre–octobre (avant gelées)",
        "exposition": "Plein soleil",
        "arrosage": "Abondant mais en profondeur",
        "espacement": "1,5–2 m entre les plants",
        "associations_positives": ["Maïs", "Haricots", "Capucines"],
        "associations_negatives": ["Pommes de terre", "Fenouil"],
        "maladies": "Oïdium en fin de saison (normal)",
        "conseil": "Plantez sur une butte de compost. En été, orientez les fruits vers le soleil pour une belle coloration.",
    },
    "Radis": {
        "emoji": "🌱",
        "description": "Le radis est la culture la plus rapide du jardin : 4 semaines de la graine à l'assiette. Parfait pour les enfants.",
        "semis": "Mars–septembre en place (toutes les 2–3 semaines)",
        "plantation": "Semis direct uniquement",
        "recolte": "4–6 semaines après semis",
        "exposition": "Soleil ou mi-ombre",
        "arrosage": "Régulier — la sécheresse les fait monter en graine",
        "espacement": "3–4 cm après éclaircissage",
        "associations_positives": ["Laitues", "Carottes", "Tomates", "Courgettes"],
        "associations_negatives": ["Hysope"],
        "maladies": "Altises (petits trous dans les feuilles)",
        "conseil": "Semez en intercalaire partout dans le potager : ils signalent par leur croissance si le sol est sain.",
    },
    "Fraise": {
        "emoji": "🍓",
        "description": "La fraise est un incontournable du jardin gourmand. Facile à cultiver, elle se renouvelle par stolons.",
        "semis": "Par stolons ou plants achetés",
        "plantation": "Août–septembre (pour récolte l'année suivante), ou mars–avril",
        "recolte": "Mai–juillet (juin–août pour remontantes)",
        "exposition": "Soleil",
        "arrosage": "Régulier, au pied — éviter les fruits",
        "espacement": "30–40 cm",
        "associations_positives": ["Laitues", "Épinards", "Ail", "Bourrache"],
        "associations_negatives": ["Choux", "Fenouil"],
        "maladies": "Botrytis (moisissure grise), oïdium",
        "conseil": "Paillez sous les fruits avec de la paille. Supprimez les stolons pendant la fructification, plantez-les en août.",
    },
}

ASSOCIATIONS = [
    {"plante1": "Tomate 🍅", "plante2": "Basilic 🌿", "effet": "✅ Le basilic repousse les pucerons et améliore le goût des tomates."},
    {"plante1": "Carotte 🥕", "plante2": "Oignon 🧅", "effet": "✅ La carotte repousse la mouche de l'oignon, l'oignon repousse la mouche de la carotte."},
    {"plante1": "Chou 🥬", "plante2": "Tomate 🍅", "effet": "❌ La tomate inhibe la croissance des choux."},
    {"plante1": "Haricot 🫘", "plante2": "Maïs 🌽", "effet": "✅ Le haricot fixe l'azote qui nourrit le maïs."},
    {"plante1": "Courgette 🥒", "plante2": "Capucine 🌸", "effet": "✅ La capucine attire les pucerons loin des courgettes."},
    {"plante1": "Pomme de terre 🥔", "plante2": "Tomate 🍅", "effet": "❌ Même famille (solanacées) — partagent les mêmes maladies (mildiou)."},
    {"plante1": "Fraise 🍓", "plante2": "Ail 🧄", "effet": "✅ L'ail protège les fraisiers contre les maladies fongiques."},
    {"plante1": "Fenouil 🌿", "plante2": "Tout le monde", "effet": "❌ Le fenouil inhibe presque toutes les autres cultures — isolez-le."},
    {"plante1": "Laitue 🥬", "plante2": "Radis 🌱", "effet": "✅ Le radis ameublit le sol au profit de la laitue."},
    {"plante1": "Rosier 🌹", "plante2": "Ail 🧄", "effet": "✅ L'ail planté au pied des rosiers prévient la maladie des taches noires."},
]

NUISIBLES = [
    {
        "nom": "Pucerons",
        "emoji": "🐛",
        "description": "Petits insectes verts, noirs ou rouges qui s'agglutinent sur les jeunes pousses et les bourgeons.",
        "degats": "Déformation des feuilles, transmission de virus, fumagine (champignon noir sur le miellat)",
        "solutions": [
            "Purin d'ortie dilué (20 ml/L) en pulvérisation",
            "Savon noir (1 c.à.s. / 1L d'eau) en pulvérisation",
            "Favoriser les coccinelles, chrysopes et syrphes",
            "Planter de la capucine comme plante-piège",
            "Jet d'eau fort pour les décrocher",
        ],
    },
    {
        "nom": "Limaces & Escargots",
        "emoji": "🐌",
        "description": "Mollusques nocturnes qui ravagent les jeunes plants, surtout par temps humide.",
        "degats": "Feuilles trouées, plants coupés au ras du sol, semis détruits",
        "solutions": [
            "Cendres de bois autour des plants (barrière à renouveler)",
            "Coquilles d'œufs broyées grossièrement",
            "Feuilles de fougère en paillis",
            "Granulés de métaldéhyde (avec précaution) ou de phosphate ferrique (sans danger)",
            "Pièges à bière (soucoupes enfoncées dans le sol)",
            "Ramassage nocturne à la lampe de poche",
        ],
    },
    {
        "nom": "Mildiou",
        "emoji": "🍂",
        "description": "Champignon redoutable qui touche les tomates, pommes de terre et vignes. Se développe par temps chaud et humide.",
        "degats": "Taches brunes sur les feuilles et tiges, pourriture rapide des fruits",
        "solutions": [
            "Bouillie bordelaise en prévention (avant les pluies)",
            "Éviter de mouiller les feuilles en arrosant",
            "Supprimer les feuilles atteintes et les brûler",
            "Bonne aération des plants (ne pas trop serrer)",
            "Choisir des variétés résistantes",
            "Rotation des cultures (ne pas replanter tomates/pommes de terre au même endroit)",
        ],
    },
    {
        "nom": "Doryphore",
        "emoji": "🪲",
        "description": "Coléoptère rayé jaune et noir, ravageur des pommes de terre et aubergines.",
        "degats": "Feuilles entièrement dévorées, plant affaibli voire mort",
        "solutions": [
            "Ramassage manuel des adultes et des pontes orange (sous les feuilles)",
            "Purin de tanaisie en pulvérisation répulsive",
            "Huile de neem (azadirachtine) — traitement naturel efficace",
            "Rotation des cultures stricte",
            "Paillage épais qui perturbe l'hivernage des larves",
        ],
    },
    {
        "nom": "Oïdium",
        "emoji": "🌫️",
        "description": "Champignon qui forme une poudre blanche sur les feuilles. Fréquent sur courgettes, rosiers, courges.",
        "degats": "Affaiblissement de la plante, mort des feuilles touchées",
        "solutions": [
            "Lait dilué (1/3 lait, 2/3 eau) en pulvérisation hebdomadaire",
            "Bicarbonate de soude (1 c.à.c. / 1L d'eau + quelques gouttes de savon noir)",
            "Décoction de prêle (antifongique naturel puissant)",
            "Supprimer les feuilles très atteintes",
            "Aérer les plants en taillant légèrement",
        ],
    },
    {
        "nom": "Mouche de la carotte",
        "emoji": "🦟",
        "description": "Petite mouche dont les larves creusent des galeries dans les carottes.",
        "degats": "Carottes trouées et brunies de l'intérieur, totalement impropres à la consommation",
        "solutions": [
            "Filet anti-insectes dès le semis (solution la plus efficace)",
            "Associer carottes et oignons / poireaux",
            "Semer en juin (après le premier vol de mai)",
            "Éviter de laisser des fanes à proximité",
        ],
    },
    {
        "nom": "Taupins (vers fil de fer)",
        "emoji": "🐛",
        "description": "Larves de coléoptère, jaunâtres et dures, qui vivent plusieurs années dans le sol.",
        "degats": "Galeries dans les tubercules (pommes de terre, carottes), plants qui fanent",
        "solutions": [
            "Enfouir des morceaux de pomme de terre comme piège et les retirer régulièrement",
            "Retourner la terre en automne pour exposer les larves aux oiseaux",
            "Planter des tagètes (œillets d'Inde) dont les racines sont répulsives",
            "Éviter les sols trop riches en matières organiques non décomposées",
        ],
    },
]

TRAITEMENTS_NATURELS = [
    {
        "nom": "Purin d'ortie",
        "emoji": "🌿",
        "usage": "Engrais foliaire, stimulant, répulsif pucerons",
        "recette": "1 kg d'orties fraîches dans 10 L d'eau. Laisser fermenter 10–15 jours à l'ombre en remuant. Filtrer. Diluer à 10% pour engrais, 5% en répulsif.",
        "application": "Pulvérisation sur feuilles ou arrosage au pied",
    },
    {
        "nom": "Purin de prêle",
        "emoji": "🌾",
        "usage": "Antifongique, fortifiant, contre mildiou et oïdium",
        "recette": "100g de prêle sèche dans 1L d'eau. Faire bouillir 20 min. Filtrer. Diluer à 20%.",
        "application": "Pulvérisation préventive tous les 15 jours",
    },
    {
        "nom": "Bouillie bordelaise",
        "emoji": "🔵",
        "usage": "Fongicide contre mildiou, tavelure, cloque du pêcher",
        "recette": "Disponible prête à l'emploi. Ou : 100g de sulfate de cuivre + 100g de chaux vive dans 10L d'eau.",
        "application": "Pulvérisation préventive avant les pluies, max 3 fois/an",
    },
    {
        "nom": "Savon noir",
        "emoji": "🧼",
        "usage": "Insecticide doux contre pucerons, acariens, cochenilles",
        "recette": "1 cuillère à soupe de savon noir liquide dans 1 litre d'eau tiède. Mélanger.",
        "application": "Pulvérisation directe sur les colonies, le matin. Rincer 48h après.",
    },
    {
        "nom": "Bicarbonate de soude",
        "emoji": "🧂",
        "usage": "Antifongique léger contre oïdium",
        "recette": "1 cuillère à café de bicarbonate + 1 litre d'eau + quelques gouttes de savon noir.",
        "application": "Pulvérisation hebdomadaire sur les feuilles atteintes",
    },
    {
        "nom": "Cendres de bois",
        "emoji": "⚪",
        "usage": "Barrière anti-limaces, apport de potasse",
        "recette": "Cendres de bois non traitées refroidies. Saupoudrer autour des plants.",
        "application": "Cercle autour des plants à renouveler après la pluie",
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# CSS et HTML
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
    /* Cacher barre d'outils Streamlit */
    header { display: none !important; }
    #MainMenu { display: none !important; }
    footer { display: none !important; }
    [data-testid="stSidebar"] { display: none !important; }

    /* Fond général */
    .stApp { background-color: #0d1f0d; color: #f0f0f0; }

    /* Titres */
    h1 { color: #4caf50 !important; text-align: center; }
    h2 { color: #81c784 !important; }
    h3 { color: #a5d6a7 !important; }

    /* Cartes */
    .card {
        background: #1a3a1a;
        border-radius: 16px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid #2e5c2e;
    }
    .card-item {
        background: #2e5c2e;
        border-radius: 10px;
        padding: 12px 16px;
        margin: 6px 0;
        border-left: 4px solid #4caf50;
    }
    .conseil-box {
        background: linear-gradient(135deg, #1a3a1a, #2e5c2e);
        border-radius: 12px;
        padding: 18px;
        border-left: 4px solid #8bc34a;
        font-style: italic;
        font-size: 1.05rem;
        margin: 12px 0;
    }
    .tag-positif { color: #69f0ae; font-weight: bold; }
    .tag-negatif { color: #ff5252; font-weight: bold; }
    .label { color: #a5d6a7; font-size: 0.9rem; }

    /* Boutons navigation */
    .stButton>button {
        background: linear-gradient(135deg, #2e7d32, #4caf50);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 0.95rem;
        font-weight: bold;
        width: 100%;
        cursor: pointer;
    }
    .stButton>button:hover { opacity: 0.85; }

    /* Séparateur */
    hr { border-color: #2e5c2e !important; }

    /* Conteneur principal */
    .block-container { padding-top: 1rem !important; }

    /* Mobile */
    @media (max-width: 768px) {
        h1 { font-size: 1.5rem !important; }
        h2 { font-size: 1.1rem !important; }
        .card { padding: 14px !important; }
        .stButton>button { font-size: 0.85rem !important; padding: 8px 6px !important; }
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# NAVIGATION
# ─────────────────────────────────────────────────────────────────────────────

if "page" not in st.session_state:
    st.session_state.page = "🏠 Accueil"

pages = ["🏠 Accueil", "📅 Calendrier", "🥕 Légumes", "🤝 Associations", "🐛 Nuisibles & Soins"]

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("🏠 Accueil", key="nav_accueil", use_container_width=True):
        st.session_state.page = "🏠 Accueil"
        st.rerun()
with col2:
    if st.button("📅 Calendrier", key="nav_cal", use_container_width=True):
        st.session_state.page = "📅 Calendrier"
        st.rerun()
with col3:
    if st.button("🥕 Légumes", key="nav_leg", use_container_width=True):
        st.session_state.page = "🥕 Légumes"
        st.rerun()
with col4:
    if st.button("🤝 Associations", key="nav_assoc", use_container_width=True):
        st.session_state.page = "🤝 Associations"
        st.rerun()
with col5:
    if st.button("🐛 Nuisibles", key="nav_nuis", use_container_width=True):
        st.session_state.page = "🐛 Nuisibles & Soins"
        st.rerun()

st.markdown("---")

page = st.session_state.page

# ─────────────────────────────────────────────────────────────────────────────
# PAGE : ACCUEIL
# ─────────────────────────────────────────────────────────────────────────────

if page == "🏠 Accueil":
    st.title("🌱 Jardiner Simplement")
    st.markdown(
        "<p style='text-align:center; color:#a5d6a7; font-size:1.1rem;'>"
        "Astuces naturelles et conseils pratiques pour un jardin qui vous ressemble."
        "</p>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # Conseil du jour
    today = date.today()
    conseil = CONSEILS_DU_JOUR[today.timetuple().tm_yday % len(CONSEILS_DU_JOUR)]

    st.markdown("### 💡 Conseil du jour")
    st.markdown(f'<div class="conseil-box">🌿 {conseil}</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Saison en cours
    mois = today.month
    info_mois = CALENDRIER[mois]

    st.markdown(f"### 🗓️ En ce mois de {info_mois['nom']}")
    st.markdown(f'<div class="card"><em>{info_mois["conseil"]}</em></div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        if info_mois["semis"]:
            st.markdown("**🌱 À semer**")
            for s in info_mois["semis"][:4]:
                st.markdown(f'<div class="card-item">{s}</div>', unsafe_allow_html=True)
        if info_mois["planter"]:
            st.markdown("**🪴 À planter**")
            for p in info_mois["planter"][:3]:
                st.markdown(f'<div class="card-item">{p}</div>', unsafe_allow_html=True)

    with col_b:
        if info_mois["recolter"]:
            st.markdown("**🧺 À récolter**")
            for r in info_mois["recolter"][:4]:
                st.markdown(f'<div class="card-item">{r}</div>', unsafe_allow_html=True)
        if info_mois["travaux"]:
            st.markdown("**🔧 Travaux**")
            for t in info_mois["travaux"][:3]:
                st.markdown(f'<div class="card-item">{t}</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Accès rapide
    st.markdown("### 🗺️ Explorer le site")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="card" style="text-align:center"><div style="font-size:2rem">📅</div><strong>Calendrier</strong><br><span class="label">Mois par mois</span></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card" style="text-align:center"><div style="font-size:2rem">🥕</div><strong>Légumes</strong><br><span class="label">Guide complet</span></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="card" style="text-align:center"><div style="font-size:2rem">🤝</div><strong>Associations</strong><br><span class="label">Bons voisins</span></div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="card" style="text-align:center"><div style="font-size:2rem">🐛</div><strong>Nuisibles</strong><br><span class="label">Remèdes naturels</span></div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE : CALENDRIER
# ─────────────────────────────────────────────────────────────────────────────

elif page == "📅 Calendrier":
    st.title("📅 Calendrier du Jardinier")
    st.markdown("<p style='text-align:center; color:#a5d6a7;'>Que faire au jardin chaque mois de l'année ?</p>", unsafe_allow_html=True)

    mois_noms = [CALENDRIER[m]["nom"] for m in range(1, 13)]
    mois_selectionne = st.selectbox(
        "Choisissez un mois",
        options=list(range(1, 13)),
        format_func=lambda m: CALENDRIER[m]["nom"],
        index=date.today().month - 1,
    )

    info = CALENDRIER[mois_selectionne]

    st.markdown(f'<div class="conseil-box">💬 {info["conseil"]}</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🌱 Semis")
        if info["semis"]:
            for s in info["semis"]:
                st.markdown(f'<div class="card-item">{s}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="card-item" style="color:#888">Pas de semis ce mois-ci.</div>', unsafe_allow_html=True)

        st.markdown("#### 🪴 Plantations")
        if info["planter"]:
            for p in info["planter"]:
                st.markdown(f'<div class="card-item">{p}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="card-item" style="color:#888">Pas de plantations ce mois-ci.</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("#### 🧺 Récoltes")
        if info["recolter"]:
            for r in info["recolter"]:
                st.markdown(f'<div class="card-item">{r}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="card-item" style="color:#888">Pas de récoltes ce mois-ci.</div>', unsafe_allow_html=True)

        st.markdown("#### 🔧 Travaux")
        if info["travaux"]:
            for t in info["travaux"]:
                st.markdown(f'<div class="card-item">{t}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Vue annuelle rapide")
    for m in range(1, 13):
        with st.expander(f"**{CALENDRIER[m]['nom']}**"):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Semis :** " + ", ".join(CALENDRIER[m]["semis"][:3]) if CALENDRIER[m]["semis"] else "*—*")
                st.markdown("**Plantations :** " + ", ".join(CALENDRIER[m]["planter"][:3]) if CALENDRIER[m]["planter"] else "*—*")
            with c2:
                st.markdown("**Récoltes :** " + ", ".join(CALENDRIER[m]["recolter"][:3]) if CALENDRIER[m]["recolter"] else "*—*")
                st.markdown("**Travaux :** " + ", ".join(CALENDRIER[m]["travaux"][:2]) if CALENDRIER[m]["travaux"] else "*—*")


# ─────────────────────────────────────────────────────────────────────────────
# PAGE : LÉGUMES
# ─────────────────────────────────────────────────────────────────────────────

elif page == "🥕 Légumes":
    st.title("🥕 Guide des Légumes")
    st.markdown("<p style='text-align:center; color:#a5d6a7;'>Tout savoir pour cultiver vos légumes avec succès.</p>", unsafe_allow_html=True)

    legume_choisi = st.selectbox(
        "Choisissez un légume",
        options=list(LEGUMES.keys()),
        format_func=lambda l: f"{LEGUMES[l]['emoji']} {l}",
    )

    l = LEGUMES[legume_choisi]

    st.markdown(f"## {l['emoji']} {legume_choisi}")
    st.markdown(f'<div class="card">{l["description"]}</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📆 Calendrier cultural")
        st.markdown(f'<div class="card-item">🌱 <strong>Semis :</strong> {l["semis"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="card-item">🪴 <strong>Plantation :</strong> {l["plantation"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="card-item">🧺 <strong>Récolte :</strong> {l["recolte"]}</div>', unsafe_allow_html=True)

        st.markdown("#### 🌍 Conditions")
        st.markdown(f'<div class="card-item">☀️ <strong>Exposition :</strong> {l["exposition"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="card-item">💧 <strong>Arrosage :</strong> {l["arrosage"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="card-item">📏 <strong>Espacement :</strong> {l["espacement"]}</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("#### 🤝 Associations")
        st.markdown("**Bons voisins :**")
        for a in l["associations_positives"]:
            st.markdown(f'<div class="card-item"><span class="tag-positif">✅</span> {a}</div>', unsafe_allow_html=True)
        st.markdown("**À éviter :**")
        for a in l["associations_negatives"]:
            st.markdown(f'<div class="card-item"><span class="tag-negatif">❌</span> {a}</div>', unsafe_allow_html=True)

        st.markdown("#### ⚠️ Maladies fréquentes")
        st.markdown(f'<div class="card-item">🔴 {l["maladies"]}</div>', unsafe_allow_html=True)

    st.markdown("#### 💡 Conseil expert")
    st.markdown(f'<div class="conseil-box">🌿 {l["conseil"]}</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE : ASSOCIATIONS
# ─────────────────────────────────────────────────────────────────────────────

elif page == "🤝 Associations":
    st.title("🤝 Associations de Plantes")
    st.markdown(
        "<p style='text-align:center; color:#a5d6a7;'>"
        "Certaines plantes s'entraident, d'autres se nuisent. "
        "Le bon voisinage, c'est la base du jardin en bonne santé."
        "</p>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    for assoc in ASSOCIATIONS:
        effet = assoc["effet"]
        if "✅" in effet:
            couleur = "#1b4332"
            icon_color = "#69f0ae"
        else:
            couleur = "#3b1a1a"
            icon_color = "#ff5252"

        st.markdown(
            f'<div class="card" style="border-left: 4px solid {icon_color}; background: {couleur};">'
            f'<strong style="font-size:1.1rem">{assoc["plante1"]} + {assoc["plante2"]}</strong><br>'
            f'<span style="color:{icon_color}">{effet}</span>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.markdown("### 📌 Principes généraux")
    principes = [
        "🌿 **Les aromates** (basilic, persil, ciboulette) sont d'excellents compagnons pour la plupart des légumes.",
        "🌸 **Les fleurs** (capucines, soucis, œillets d'Inde) dans le potager attirent les insectes utiles et repoussent les nuisibles.",
        "🚫 **Le fenouil** est l'ennemi commun — plantez-le toujours seul, à l'écart.",
        "🔄 **La rotation** : ne replantez jamais la même famille au même endroit deux années de suite.",
        "🐝 **Les plantes à fleurs** dans et autour du potager attirent les pollinisateurs indispensables.",
        "💪 **Les légumineuses** (haricots, pois, fèves) enrichissent le sol en azote au profit de leurs voisins.",
    ]
    for p in principes:
        st.markdown(f'<div class="card-item">{p}</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE : NUISIBLES & SOINS
# ─────────────────────────────────────────────────────────────────────────────

elif page == "🐛 Nuisibles & Soins":
    st.title("🐛 Nuisibles & Traitements Naturels")
    st.markdown(
        "<p style='text-align:center; color:#a5d6a7;'>"
        "Identifier les problèmes et y répondre sans chimie."
        "</p>",
        unsafe_allow_html=True
    )

    onglet1, onglet2 = st.tabs(["🐛 Nuisibles & Maladies", "🌿 Traitements naturels"])

    with onglet1:
        for n in NUISIBLES:
            with st.expander(f"{n['emoji']} **{n['nom']}**"):
                st.markdown(f"**Description :** {n['description']}")
                st.markdown(f"**Dégâts :** _{n['degats']}_")
                st.markdown("**Solutions naturelles :**")
                for s in n["solutions"]:
                    st.markdown(f'<div class="card-item">✅ {s}</div>', unsafe_allow_html=True)

    with onglet2:
        st.markdown("### 🧪 Recettes de traitements maison")
        for t in TRAITEMENTS_NATURELS:
            st.markdown(
                f'<div class="card">'
                f'<h3>{t["emoji"]} {t["nom"]}</h3>'
                f'<p><span class="label">Usage :</span> {t["usage"]}</p>'
                f'<p><span class="label">Recette :</span> {t["recette"]}</p>'
                f'<p><span class="label">Application :</span> {t["application"]}</p>'
                f'</div>',
                unsafe_allow_html=True
            )
