#!/usr/bin/env python3
"""Génère les trois pages d'accueil (fr, en, nl) à partir d'un seul gabarit.

Les textes vivent dans T ; le gabarit ne contient aucune phrase. Lancer
`python3 build.py` après toute modification, puis publier.
"""
import json
import pathlib
import re

BASE = "https://paperkeep.be/"
STORE = "https://chromewebstore.google.com/detail/mmllhnjkdpilogbaokplljippcnmdopi"
MAIL = "contact@paperkeep.be"
FACEBOOK = "https://www.facebook.com/1273897999150933"
GITHUB = "https://github.com/Paperkeep-app/paperkeep-extension"
AUJOURDHUI = __import__("datetime").date.today().isoformat()
FICHIER = {"fr": "index.html", "en": "en.html", "nl": "nl.html"}

T = {
    "fr": dict(
        titre="Paperkeep — vos factures fournisseurs récupérées et renommées en un clic",
        desc="Extension Chrome gratuite : sur la page de facturation de vos abonnements, un clic télécharge vos factures et les renomme par date, fournisseur et montant. Rien ne quitte votre ordinateur.",
        nav=["Fonctionnement", "Confidentialité", "Comptables", "Aide"],
        cta="Ajouter à Chrome", cta_sub="gratuit",
        oeil="Extension Chrome gratuite",
        h1a="Vos factures fournisseurs,", h1b="récupérées en un clic.",
        chapo="Hébergement, logiciels, outils en ligne : Paperkeep va chercher les factures sur la page de facturation, les télécharge et les renomme pour votre comptable.",
        voir="Voir comment ça marche",
        gages=["Sans compte", "Rien ne quitte votre ordinateur", "Français · Nederlands · English"],
        demo_titre="Historique de facturation", demo_payee="Payée", demo_bouton="Télécharger (3)", demo_dossier="Téléchargements › Factures",
        avant="Avant", apres="Après",
        s1_oeil="Le problème", s1_h="Des fichiers que personne ne sait lire.",
        s1_p="Chaque service nomme ses factures à sa façon. Paperkeep leur donne à toutes le même nom : la date, le fournisseur, le montant. Le dossier se trie tout seul.",
        s2_oeil="Fonctionnement", s2_h="Trois gestes, pas un de plus.",
        etapes=[("Ouvrez la page de facturation", "Celle où votre service liste vos factures : « Facturation », « Historique de paiement », « Mes factures »."),
                ("Cliquez sur l'icône Paperkeep", "L'extension repère les factures de la page, avec leur date et leur montant. Décochez celles que vous avez déjà."),
                ("Récupérez le dossier", "Tout arrive dans Téléchargements › Factures, renommé et vérifié, prêt à transmettre.")],
        s3_oeil="Ce que fait Paperkeep", s3_h="Pensé pour les pages qui résistent.",
        atouts=[("Portails Stripe", "Le portail de facturation utilisé par un très grand nombre de services en ligne est reconnu d'office."),
                ("PDF caché derrière un bouton", "Quand la facture n'est pas un simple lien, Paperkeep va la chercher quand même."),
                ("Reçus sans PDF", "Certains services n'offrent qu'un reçu à l'écran. La page est enregistrée telle quelle, dans un fichier unique."),
                ("Chaque fichier vérifié", "Un téléchargement vide ou qui n'est pas un document vous est signalé, au lieu de passer pour une facture."),
                ("Vous choisissez", "Toutes les factures trouvées sont cochées ; décochez celles dont vous n'avez pas besoin."),
                ("Trois langues", "Interface en français, en néerlandais et en anglais, selon la langue de votre navigateur.")],
        s4_oeil="Confidentialité", s4_h="Rien ne quitte votre ordinateur.",
        s4_p="Paperkeep n'a ni compte, ni serveur, ni statistiques. Vos factures vont de la page à votre dossier, sans passer par nous.",
        prive=[("Aucun compte", "Rien à créer, rien à connecter."),
               ("Lecture au clic", "La page n'est lue qu'au moment où vous cliquez sur l'icône."),
               ("Accès demandé site par site", "Rien n'est demandé à l'installation. Vous pouvez toujours refuser.")],
        prive_lien="Lire la politique de confidentialité", code_lien="Vérifier dans le code source",
        s5_oeil="Pour les comptables", s5_h="Vos clients oublient leurs factures d'achat ?",
        s5_p="Envoyez-leur le lien. Ils récupèrent en un clic les factures de leurs abonnements et vous transmettent un dossier propre. Un fournisseur manque ? Dites-le-nous, nous ajoutons en priorité ceux que vos clients utilisent.",
        s5_cta="Nous écrire",
        capture_alt="Paperkeep ouvert sur une page de facturation : quatre factures détectées avec leur date",
        capture_leg="L'extension sur une page de facturation.",
        faq_h="Questions fréquentes",
        faq=[("Est-ce gratuit ?", "Oui, sans compte et sans limite de téléchargements. Une formule payante pour les gros volumes et les cabinets comptables viendra plus tard ; ce que vous avez déjà récupéré reste à vous."),
             ("Sur quels services ça marche ?", "Sur les portails de facturation Stripe, sur les pages qui listent des factures en PDF et sur celles dont les liens n'ont pas d'extension. Si un service n'est pas reconnu, écrivez-nous : nous l'ajoutons."),
             ("Où arrivent mes factures ?", "Dans le dossier Téléchargements › Factures de votre ordinateur, sous la forme 2026-09-06_fournisseur_15-00EUR.pdf."),
             ("Mes données sont-elles envoyées quelque part ?", "Non. Aucun serveur, aucune statistique. Les fichiers vont directement dans votre dossier Téléchargements.")],
        faq_plus="Toutes les questions et le contact",
        fin_h="Dix minutes par mois, et le dossier est prêt.", fin_p="Installez Paperkeep, ouvrez une page de facturation, cliquez.",
        pied=["Aide et contact", "Guides", "À propos", "Confidentialité"], pied_liens=["aide.html", "guides.html", "a-propos.html", "privacy.html"],
        mention="Paperkeep — Talal Swalha, numéro d'entreprise BE 1042.078.027, Ixelles (Belgique).",
        fournisseur="fournisseur",
    ),
    "en": dict(
        titre="Paperkeep — your supplier invoices collected and renamed in one click",
        desc="Free Chrome extension: on the billing page of your subscriptions, one click downloads your invoices and renames them by date, vendor and amount. Nothing leaves your computer.",
        nav=["How it works", "Privacy", "Accountants", "Help"],
        cta="Add to Chrome", cta_sub="free",
        oeil="Free Chrome extension",
        h1a="Your supplier invoices,", h1b="collected in one click.",
        chapo="Hosting, software, online tools: Paperkeep finds the invoices on the billing page, downloads them and renames them for your accountant.",
        voir="See how it works",
        gages=["No account", "Nothing leaves your computer", "English · Français · Nederlands"],
        demo_titre="Billing history", demo_payee="Paid", demo_bouton="Download (3)", demo_dossier="Downloads › Factures",
        avant="Before", apres="After",
        s1_oeil="The problem", s1_h="Files nobody can read.",
        s1_p="Every service names its invoices its own way. Paperkeep gives them all the same name: date, vendor, amount. The folder sorts itself.",
        s2_oeil="How it works", s2_h="Three steps, not one more.",
        etapes=[("Open the billing page", "The one where your service lists your invoices: “Billing”, “Payment history”, “Invoices”."),
                ("Click the Paperkeep icon", "The extension finds the invoices on the page, with their date and amount. Untick the ones you already have."),
                ("Collect the folder", "Everything lands in Downloads › Factures, renamed and checked, ready to hand over.")],
        s3_oeil="What Paperkeep does", s3_h="Built for the pages that resist.",
        atouts=[("Stripe portals", "The billing portal used by a very large number of online services is recognised out of the box."),
                ("PDF hidden behind a button", "When the invoice is not a plain link, Paperkeep still goes and gets it."),
                ("Receipts without a PDF", "Some services only show a receipt on screen. The page is saved as it is, in a single file."),
                ("Every file checked", "An empty download, or one that is not a document, is flagged instead of passing for an invoice."),
                ("You choose", "Every invoice found is ticked; untick the ones you do not need."),
                ("Three languages", "Interface in English, French and Dutch, following your browser language.")],
        s4_oeil="Privacy", s4_h="Nothing leaves your computer.",
        s4_p="Paperkeep has no account, no server and no analytics. Your invoices go from the page to your folder, without passing through us.",
        prive=[("No account", "Nothing to create, nothing to connect."),
               ("Read on click", "The page is only read when you click the icon."),
               ("Access asked site by site", "Nothing is requested at install. You can always decline.")],
        prive_lien="Read the privacy policy", code_lien="Check it in the source code",
        s5_oeil="For accountants", s5_h="Clients who forget their purchase invoices?",
        s5_p="Send them the link. In one click they collect the invoices of their subscriptions and hand you a clean folder. A provider is missing? Tell us: we add the ones your clients use first.",
        s5_cta="Write to us",
        capture_alt="Paperkeep open on a billing page: four invoices detected with their date",
        capture_leg="The extension on a billing page.",
        faq_h="Frequently asked questions",
        faq=[("Is it free?", "Yes, with no account and no download limit. A paid plan for high volumes and accounting firms will come later; what you have already collected stays yours."),
             ("Which services does it work on?", "On Stripe billing portals, on pages listing PDF invoices and on pages whose links have no file extension. If a service is not recognised, write to us: we add it."),
             ("Where do my invoices go?", "To the Downloads › Factures folder on your computer, named 2026-09-06_vendor_15-00EUR.pdf."),
             ("Is my data sent anywhere?", "No. No server, no analytics. Files go straight to your Downloads folder.")],
        faq_plus="All questions and contact",
        fin_h="Ten minutes a month, and the folder is ready.", fin_p="Install Paperkeep, open a billing page, click.",
        pied=["Help and contact", "Privacy"], pied_liens=["aide.html#en", "privacy.html"],
        mention="Paperkeep — Talal Swalha, company number BE 1042.078.027, Ixelles (Belgium).",
        fournisseur="vendor",
    ),
    "nl": dict(
        titre="Paperkeep — je leveranciersfacturen opgehaald en hernoemd met één klik",
        desc="Gratis Chrome-extensie: op de facturatiepagina van je abonnementen downloadt één klik je facturen en hernoemt ze op datum, leverancier en bedrag. Er verlaat niets je computer.",
        nav=["Hoe het werkt", "Privacy", "Boekhouders", "Hulp"],
        cta="Toevoegen aan Chrome", cta_sub="gratis",
        oeil="Gratis Chrome-extensie",
        h1a="Je leveranciersfacturen,", h1b="opgehaald met één klik.",
        chapo="Hosting, software, online tools: Paperkeep vindt de facturen op de facturatiepagina, downloadt ze en hernoemt ze voor je boekhouder.",
        voir="Bekijk hoe het werkt",
        gages=["Geen account", "Er verlaat niets je computer", "Nederlands · Français · English"],
        demo_titre="Factuurgeschiedenis", demo_payee="Betaald", demo_bouton="Downloaden (3)", demo_dossier="Downloads › Factures",
        avant="Voor", apres="Na",
        s1_oeil="Het probleem", s1_h="Bestanden die niemand kan lezen.",
        s1_p="Elke dienst geeft zijn facturen een eigen naam. Paperkeep geeft ze allemaal dezelfde: datum, leverancier, bedrag. De map sorteert zichzelf.",
        s2_oeil="Hoe het werkt", s2_h="Drie stappen, niet één meer.",
        etapes=[("Open de facturatiepagina", "De pagina waar je dienst je facturen toont: “Facturatie”, “Betaalgeschiedenis”, “Facturen”."),
                ("Klik op het Paperkeep-icoon", "De extensie vindt de facturen op de pagina, met datum en bedrag. Vink uit wat je al hebt."),
                ("Haal de map op", "Alles komt in Downloads › Factures terecht, hernoemd en gecontroleerd, klaar om door te geven.")],
        s3_oeil="Wat Paperkeep doet", s3_h="Gemaakt voor pagina's die tegenwerken.",
        atouts=[("Stripe-portalen", "Het facturatieportaal dat heel veel online diensten gebruiken, wordt meteen herkend."),
                ("Pdf achter een knop", "Is de factuur geen gewone link, dan haalt Paperkeep ze toch op."),
                ("Bonnen zonder pdf", "Sommige diensten tonen alleen een bon op het scherm. De pagina wordt bewaard zoals ze is, in één bestand."),
                ("Elk bestand gecontroleerd", "Een lege download, of een die geen document is, wordt gemeld in plaats van door te gaan voor een factuur."),
                ("Jij kiest", "Alle gevonden facturen zijn aangevinkt; vink uit wat je niet nodig hebt."),
                ("Drie talen", "Interface in het Nederlands, Frans en Engels, volgens de taal van je browser.")],
        s4_oeil="Privacy", s4_h="Er verlaat niets je computer.",
        s4_p="Paperkeep heeft geen account, geen server en geen statistieken. Je facturen gaan van de pagina naar je map, zonder langs ons te gaan.",
        prive=[("Geen account", "Niets aan te maken, niets te koppelen."),
               ("Lezen bij de klik", "De pagina wordt alleen gelezen wanneer je op het icoon klikt."),
               ("Toegang per site gevraagd", "Bij de installatie wordt niets gevraagd. Je kunt altijd weigeren.")],
        prive_lien="Lees het privacybeleid", code_lien="Controleer het in de broncode",
        s5_oeil="Voor boekhouders", s5_h="Klanten die hun aankoopfacturen vergeten?",
        s5_p="Bezorg hun de link. Met één klik halen ze de facturen van hun abonnementen op en bezorgen ze u een nette map. Ontbreekt er een leverancier? Laat het ons weten: we voegen eerst toe wat uw klanten gebruiken.",
        s5_cta="Schrijf ons",
        capture_alt="Paperkeep geopend op een facturatiepagina: vier facturen gevonden met hun datum",
        capture_leg="De extensie op een facturatiepagina.",
        faq_h="Veelgestelde vragen",
        faq=[("Is het gratis?", "Ja, zonder account en zonder downloadlimiet. Een betaalde formule voor grote volumes en boekhoudkantoren volgt later; wat je al hebt opgehaald, blijft van jou."),
             ("Op welke diensten werkt het?", "Op Stripe-portalen, op pagina's met facturen in pdf en op pagina's waarvan de links geen extensie hebben. Wordt een dienst niet herkend, schrijf ons dan: we voegen hem toe."),
             ("Waar komen mijn facturen terecht?", "In de map Downloads › Factures op je computer, met de naam 2026-09-06_leverancier_15-00EUR.pdf."),
             ("Worden mijn gegevens ergens naartoe gestuurd?", "Nee. Geen server, geen statistieken. De bestanden gaan rechtstreeks naar je map Downloads.")],
        faq_plus="Alle vragen en contact",
        fin_h="Tien minuten per maand, en de map is klaar.", fin_p="Installeer Paperkeep, open een facturatiepagina, klik.",
        pied=["Hulp en contact", "Gids", "Privacy"], pied_liens=["aide.html#nl", "gids-facturen-abonnementen.html", "privacy.html"],
        mention="Paperkeep — Talal Swalha, ondernemingsnummer BE 1042.078.027, Elsene (België).",
        fournisseur="leverancier",
    ),
}

LOGO = ('<svg width="34" height="34" viewBox="0 0 128 128" aria-hidden="true"><rect x="4" y="4" width="120" height="120" rx="28" fill="#1E5142"/>'
        '<path d="M36 30a6 6 0 0 1 6-6h44a6 6 0 0 1 6 6v70l-7-5-7 5-7-5-7 5-7-5-7 5-7-5-7 5V30z" fill="#fff"/>'
        '<path d="M47 42h34M47 53h22" stroke="#1E5142" stroke-width="6" stroke-linecap="round"/>'
        '<path d="M64 62v20m-9-9l9 9 9-9" stroke="#1E5142" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>')

ICONES = [
    '<path d="M4 7h16M4 12h16M4 17h10"/>',
    '<path d="M12 4v11m-4-4 4 4 4-4M5 20h14"/>',
    '<path d="M6 3h12v18l-3-2-3 2-3-2-3 2zM9 8h6M9 12h4"/>',
    '<path d="m5 12 4 4 10-10"/>',
    '<path d="M4 6h3v3H4zM4 15h3v3H4zM11 7h9M11 16h9"/>',
    '<path d="M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18zM3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>',
]

CSS = r"""
:root{--encre:#0f1f1a;--vert:#1E5142;--vert-nuit:#0c2a21;--menthe:#bff0d6;--citron:#d9f36a;--creme:#f6f4ee;--papier:#fff;--gris:#5d6964;--trait:#e2e5e0;--rayon:18px}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;overflow-x:hidden;font:17px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,sans-serif;color:var(--encre);background:var(--creme);-webkit-font-smoothing:antialiased}
a{color:inherit}img{max-width:100%;display:block}
.w{max-width:1120px;margin:0 auto;padding-inline:24px}
h1,h2,h3{letter-spacing:-.025em;line-height:1.08;margin:0}
.oeil{font-size:13px;font-weight:650;letter-spacing:.09em;text-transform:uppercase;color:var(--vert);margin:0 0 14px}
.btn{display:inline-flex;align-items:center;gap:10px;padding:14px 22px;border-radius:999px;background:var(--citron);color:var(--encre);font-weight:650;text-decoration:none;transition:transform .2s,box-shadow .2s;box-shadow:0 1px 0 rgba(0,0,0,.08)}
.btn:hover{transform:translateY(-2px);box-shadow:0 10px 24px -10px rgba(217,243,106,.9)}
.btn small{font-weight:500;opacity:.7;font-size:14px}
.btn.sombre{background:var(--vert);color:#fff}.btn.sombre:hover{box-shadow:0 10px 24px -10px rgba(30,81,66,.8)}
.lien{font-weight:600;text-decoration:none;border-bottom:1.5px solid currentColor;padding-bottom:1px}

/* barre */
.barre{position:sticky;top:0;z-index:20;background:rgba(12,42,33,.86);backdrop-filter:saturate(1.4) blur(12px);-webkit-backdrop-filter:saturate(1.4) blur(12px);color:#fff}
.barre .w{display:flex;align-items:center;gap:22px;height:66px}
.marque{display:flex;align-items:center;gap:10px;font-weight:700;font-size:19px;text-decoration:none;letter-spacing:-.02em}
.barre nav{display:flex;gap:22px;margin-left:auto;font-size:15px}
.barre nav a{text-decoration:none;opacity:.78}.barre nav a:hover{opacity:1}
.langues{display:flex;gap:4px;font-size:13px;font-weight:600}
.langues a{text-decoration:none;padding:5px 8px;border-radius:8px;opacity:.6}.langues a[aria-current]{background:rgba(255,255,255,.14);opacity:1}
.barre .btn{padding:10px 16px;font-size:15px}

/* accroche */
.hero{position:relative;overflow:hidden;color:#fff;background:radial-gradient(900px 500px at 78% 8%,rgba(191,240,214,.22),transparent 60%),radial-gradient(700px 500px at 0% 100%,rgba(217,243,106,.10),transparent 60%),linear-gradient(180deg,var(--vert-nuit),#12382d 70%,#17463a)}
.hero:before{content:"";position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.05) 1px,transparent 1px);background-size:46px 46px;mask-image:radial-gradient(ellipse at 60% 30%,#000 10%,transparent 70%);-webkit-mask-image:radial-gradient(ellipse at 60% 30%,#000 10%,transparent 70%)}
.hero .w{position:relative;display:grid;grid-template-columns:1.1fr 1fr;gap:54px;align-items:center;padding-block:78px 120px}
.hero .oeil{color:var(--menthe);display:inline-flex;align-items:center;gap:8px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.14);padding:7px 13px;border-radius:999px;letter-spacing:.06em}
.hero .oeil i{width:7px;height:7px;border-radius:50%;background:var(--citron);box-shadow:0 0 0 4px rgba(217,243,106,.2)}
.hero h1{font-size:clamp(34px,4.5vw,58px);font-weight:700;overflow-wrap:break-word;hyphens:auto}
.hero h1 span{display:block}.hero h1 .b{color:var(--menthe)}
.hero p.chapo{font-size:19px;line-height:1.55;color:rgba(255,255,255,.8);max-width:33em;margin:22px 0 30px}
.actions{display:flex;flex-wrap:wrap;gap:18px;align-items:center}
.actions .lien{color:#fff;opacity:.9}
.gages{display:flex;flex-wrap:wrap;gap:8px 20px;margin:34px 0 0;padding:0;list-style:none;font-size:14.5px;color:rgba(255,255,255,.72)}
.gages li{display:flex;align-items:center;gap:8px}.gages li:before{content:"";width:16px;height:16px;border-radius:50%;background:rgba(191,240,214,.18) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath d='m4.5 8.2 2.3 2.3 4.7-5' fill='none' stroke='%23bff0d6' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center/16px}

/* démonstration animée */
.demo{position:relative;perspective:1400px}
.fenetre{background:#fff;color:var(--encre);border-radius:16px;box-shadow:0 40px 80px -30px rgba(0,0,0,.6),0 0 0 1px rgba(255,255,255,.1);overflow:hidden;transform:rotateY(-7deg) rotateX(3deg);transform-origin:left center}
.chrome{display:flex;align-items:center;gap:7px;padding:11px 14px;background:#eef1ee;border-bottom:1px solid var(--trait)}
.chrome i{width:10px;height:10px;border-radius:50%;background:#d5dad6}.chrome b{flex:1;margin-left:8px;background:#fff;border-radius:7px;height:22px;font:500 11px/22px ui-monospace,Menlo,monospace;color:#8a948f;padding-left:10px;overflow:hidden;white-space:nowrap}
.chrome em{width:22px;height:22px;border-radius:6px;background:var(--vert);animation:pouls 8s infinite}
.page{padding:18px 20px 64px}
.page h4{margin:0 0 12px;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:#8a948f;font-weight:650}
.ligne{display:grid;grid-template-columns:1fr auto auto;gap:14px;align-items:center;padding:11px 0;border-top:1px solid var(--trait);font-size:14px}
.ligne span:nth-child(2){font-variant-numeric:tabular-nums;font-weight:600}
.ligne .ok{font-size:11px;font-weight:650;color:#1f7a4d;background:#e3f6ea;padding:3px 8px;border-radius:999px}
.bulle{position:absolute;right:-22px;top:58px;width:232px;background:#fff;color:var(--encre);border-radius:14px;padding:14px;box-shadow:0 30px 60px -20px rgba(0,0,0,.55),0 0 0 1px rgba(15,31,26,.06);animation:bulle 8s infinite}
.bulle strong{display:block;font-size:13.5px;margin-bottom:9px}
.bulle label{display:flex;align-items:center;gap:8px;font-size:12px;padding:6px 8px;border:1px solid var(--trait);border-radius:7px;margin-bottom:5px}
.bulle label:before{content:"";width:13px;height:13px;border-radius:3px;background:var(--vert) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath d='m4 8.3 2.6 2.6L12 5.3' fill='none' stroke='white' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center/13px}
.bulle label span{margin-left:auto;color:#8a948f;font-variant-numeric:tabular-nums}
.bulle button{width:100%;margin-top:5px;border:0;border-radius:8px;padding:9px;font:650 12.5px/1 inherit;background:var(--vert);color:#fff;animation:appui 8s infinite}
.fichiers{position:absolute;left:-18px;bottom:-66px;width:min(330px,82%);background:var(--encre);color:#eaf3ee;border-radius:14px;padding:13px 15px;box-shadow:0 30px 60px -20px rgba(0,0,0,.6);font:500 12px/1.9 ui-monospace,Menlo,monospace}
.fichiers small{display:block;font:650 10.5px/1 -apple-system,sans-serif;letter-spacing:.1em;text-transform:uppercase;color:var(--menthe);margin-bottom:6px}
.fichiers div{opacity:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;animation:fichier 8s infinite}
.fichiers div:nth-of-type(2){animation-delay:.35s}.fichiers div:nth-of-type(3){animation-delay:.7s}
.fichiers div:before{content:"↓ ";color:var(--citron)}
@keyframes bulle{0%,6%{opacity:0;transform:translateY(-8px) scale(.97)}12%,92%{opacity:1;transform:none}100%{opacity:0;transform:translateY(-8px) scale(.97)}}
@keyframes appui{0%,38%{transform:none;background:var(--vert)}42%{transform:scale(.96);background:#17463a}46%,100%{transform:none;background:var(--vert)}}
@keyframes fichier{0%,46%{opacity:0;transform:translateX(-10px)}54%,92%{opacity:1;transform:none}100%{opacity:0}}
@keyframes pouls{0%,4%{box-shadow:0 0 0 0 rgba(30,81,66,.5)}9%{box-shadow:0 0 0 9px rgba(30,81,66,0)}100%{box-shadow:0 0 0 0 rgba(30,81,66,0)}}

/* sections */
section{padding-block:96px}
.entete{max-width:36em;margin-bottom:46px}
.entete h2{font-size:clamp(30px,3.8vw,46px);font-weight:700}
.entete p{color:var(--gris);font-size:18.5px;margin:18px 0 0}
.avantapres{display:grid;grid-template-columns:1fr auto 1fr;gap:22px;align-items:center}
.pile{background:var(--papier);border:1px solid var(--trait);border-radius:var(--rayon);padding:22px 24px;font:500 14px/2.1 ui-monospace,Menlo,monospace}
.pile b{display:block;font:650 12px/1 -apple-system,sans-serif;letter-spacing:.09em;text-transform:uppercase;margin-bottom:12px;color:var(--gris)}
.pile div{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:#9aa39e}
.pile.propre{background:var(--encre);border-color:var(--encre)}.pile.propre b{color:var(--menthe)}.pile.propre div{color:#eaf3ee}
.fleche{width:46px;height:46px;border-radius:50%;background:var(--citron);display:grid;place-items:center;font-size:22px;font-weight:700}
.etapes{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;counter-reset:e}
.etape{background:var(--papier);border:1px solid var(--trait);border-radius:var(--rayon);padding:28px 26px 30px;counter-increment:e;transition:transform .25s,box-shadow .25s}
.etape:hover,.atout:hover{transform:translateY(-4px);box-shadow:0 22px 40px -26px rgba(15,31,26,.45)}
.etape:before{content:counter(e);display:grid;place-items:center;width:42px;height:42px;border-radius:12px;background:var(--vert);color:#fff;font-weight:700;font-size:18px;margin-bottom:20px}
.etape h3,.atout h3{font-size:20px;margin-bottom:8px}.etape p,.atout p{margin:0;color:var(--gris);font-size:16px}
.capture{margin:56px 0 0;border-radius:var(--rayon);overflow:hidden;border:1px solid var(--trait);background:#fff;box-shadow:0 40px 80px -50px rgba(15,31,26,.55)}
.capture img{width:100%;aspect-ratio:1280/540;object-fit:cover;object-position:top}
.capture figcaption{font-size:14px;color:var(--gris);padding:12px 18px;border-top:1px solid var(--trait)}
.atouts{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.atout{background:var(--papier);border:1px solid var(--trait);border-radius:var(--rayon);padding:26px;transition:transform .25s,box-shadow .25s}
.atout svg{width:26px;height:26px;stroke:var(--vert);fill:none;stroke-width:1.9;stroke-linecap:round;stroke-linejoin:round;background:#e6f3ec;border-radius:10px;padding:9px;box-sizing:content-box;margin-bottom:18px}
.sombre-s{background:var(--vert-nuit);color:#fff;border-radius:34px;margin-inline:16px;padding-block:84px}
.sombre-s .oeil{color:var(--menthe)}.sombre-s .entete p{color:rgba(255,255,255,.74)}
.prive{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-bottom:34px}
.prive div{border:1px solid rgba(255,255,255,.14);background:rgba(255,255,255,.05);border-radius:var(--rayon);padding:24px}
.prive h3{font-size:19px;margin-bottom:8px}.prive p{margin:0;color:rgba(255,255,255,.72);font-size:16px}
.sombre-s .lien{color:var(--menthe)}
.compta{display:grid;grid-template-columns:1.2fr .8fr;gap:40px;align-items:center;background:var(--papier);border:1px solid var(--trait);border-radius:28px;padding:48px}
.compta h2{font-size:clamp(28px,3.2vw,40px);font-weight:700;margin-bottom:16px}.compta p{color:var(--gris);margin:0 0 26px}
.carte-lien{background:var(--creme);border-radius:var(--rayon);padding:22px;font:500 13.5px/1.7 ui-monospace,Menlo,monospace;word-break:break-all;border:1px dashed #c9cfc9}
.carte-lien b{display:block;font:650 12px/1 -apple-system,sans-serif;letter-spacing:.09em;text-transform:uppercase;color:var(--gris);margin-bottom:10px}
.faq{max-width:780px}
details{background:var(--papier);border:1px solid var(--trait);border-radius:14px;padding:18px 22px;margin-bottom:10px}
summary{font-weight:650;cursor:pointer;list-style:none;display:flex;justify-content:space-between;gap:16px}
summary::-webkit-details-marker{display:none}summary:after{content:"+";font-size:22px;line-height:1;color:var(--vert);transition:transform .2s}
details[open] summary:after{transform:rotate(45deg)}details p{margin:12px 0 2px;color:var(--gris)}
.fin{text-align:center;padding-block:40px 110px}
.fin h2{font-size:clamp(30px,4.2vw,52px);font-weight:700;max-width:16em;margin:0 auto 14px}.fin p{color:var(--gris);font-size:19px;margin:0 0 30px}
footer{border-top:1px solid var(--trait);padding-block:34px 44px;font-size:15px;color:var(--gris)}
footer .w{display:flex;flex-wrap:wrap;gap:14px 26px;align-items:center}footer a{text-decoration:none}footer a:hover{color:var(--encre)}
footer p{margin:0;flex-basis:100%;font-size:14px}

/* apparition au défilement */
.js .r{opacity:0;transform:translateY(22px);transition:opacity .7s cubic-bezier(.16,1,.3,1),transform .7s cubic-bezier(.16,1,.3,1)}
.js .r.vu{opacity:1;transform:none}
.js .etapes .r:nth-child(2),.js .atouts .r:nth-child(3n+2),.js .prive .r:nth-child(2){transition-delay:.09s}
.js .etapes .r:nth-child(3),.js .atouts .r:nth-child(3n),.js .prive .r:nth-child(3){transition-delay:.18s}

@media (max-width:920px){
  .hero .w{grid-template-columns:1fr;padding-block:52px 96px;gap:60px}
  .fenetre{transform:none}.bulle{right:8px}.fichiers{left:8px}
  .etapes,.atouts,.prive{grid-template-columns:1fr}
  .avantapres{grid-template-columns:1fr}.fleche{margin:0 auto;transform:rotate(90deg)}
  .compta{grid-template-columns:1fr;padding:30px}
  .barre nav{display:none}.langues{margin-left:auto}
  section{padding-block:68px}.sombre-s{margin-inline:8px;border-radius:26px}
}
@media (max-width:520px){.barre .btn{display:none}.barre .w{gap:12px}.bulle{width:196px;right:4px}.fichiers{left:4px}.hero h1{font-size:31px}.hero p.chapo{font-size:17.5px}.w{padding-inline:20px}}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important;scroll-behavior:auto!important}.bulle,.fichiers div{opacity:1}.js .r{opacity:1;transform:none}}
"""

JS = ("document.documentElement.classList.add('js');"
      "if('IntersectionObserver' in window){var o=new IntersectionObserver(function(e){e.forEach(function(x){if(x.isIntersecting){x.target.classList.add('vu');o.unobserve(x.target)}})},{threshold:.12});"
      "document.querySelectorAll('.r').forEach(function(n){o.observe(n)})}else{document.querySelectorAll('.r').forEach(function(n){n.classList.add('vu')})}")

CHROME_ICO = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4v11m-4.5-4.5L12 15l4.5-4.5M5 20h14"/></svg>'


ORGANISATION = {
    "@context": "https://schema.org", "@type": "Organization", "@id": BASE + "#organisation", "name": "Paperkeep", "url": BASE,
    "logo": BASE + "img/logo-512.png", "email": MAIL, "vatID": "BE1042078027",
    "founder": {"@type": "Person", "name": "Talal Swalha"},
    "address": {"@type": "PostalAddress", "addressLocality": "Ixelles", "postalCode": "1050", "addressCountry": "BE"},
    "contactPoint": {"@type": "ContactPoint", "contactType": "customer support", "email": MAIL, "availableLanguage": ["fr", "nl", "en"]},
    "sameAs": [STORE, FACEBOOK, GITHUB],
}


def page(lang):
    t = T[lang]
    f = FICHIER[lang]
    url = BASE + ("" if lang == "fr" else f)
    alt = "".join(f'<link rel="alternate" hreflang="{l}" href="{BASE}{"" if l == "fr" else FICHIER[l]}">\n' for l in ("fr", "en", "nl"))
    alt += f'<link rel="alternate" hreflang="x-default" href="{BASE}en.html">\n'
    ld = [
        ORGANISATION,
        {"@context": "https://schema.org", "@type": "WebSite", "name": "Paperkeep", "url": BASE, "inLanguage": ["fr", "nl", "en"],
         "publisher": {"@id": BASE + "#organisation"}},
        {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "Paperkeep", "applicationCategory": "BusinessApplication",
         "dateModified": AUJOURDHUI, "author": {"@id": BASE + "#organisation"},
         "applicationSubCategory": "Browser extension", "operatingSystem": "Chrome", "inLanguage": ["fr", "nl", "en"], "description": t["desc"],
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}, "downloadUrl": STORE, "installUrl": STORE, "url": BASE,
         "image": BASE + "img/logo-512.png", "screenshot": BASE + "img/capture-detection.png",
         "publisher": {"@id": BASE + "#organisation"}},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in t["faq"]]},
    ]
    courant = ' aria-current="true"'
    langues = "".join(f'<a href="{FICHIER[l]}"{courant if l == lang else ""} lang="{l}">{l.upper()}</a>' for l in ("fr", "nl", "en"))
    v = t["fournisseur"]
    lignes = [("6 sept. 2026" if lang == "fr" else "6 Sep 2026", "29,00 €"), ("6 août 2026" if lang == "fr" else "6 Aug 2026", "29,00 €"), ("6 juil. 2026" if lang == "fr" else "6 Jul 2026", "19,00 €")]
    noms = [f"2026-09-06_{v}_29-00EUR.pdf", f"2026-08-06_{v}_29-00EUR.pdf", f"2026-07-06_{v}_19-00EUR.pdf"]
    sales = ["invoice_4821.pdf", "Receipt-2291-7743.pdf", "document (3).pdf", "F0091-2026.pdf"]
    propres = [f"2026-06-06_{v}_19-00EUR.pdf", f"2026-07-06_{v}_19-00EUR.pdf", f"2026-08-06_{v}_29-00EUR.pdf", f"2026-09-06_{v}_29-00EUR.pdf"]
    btn = f'<a class="btn" href="{STORE}">{CHROME_ICO}{t["cta"]} <small>— {t["cta_sub"]}</small></a>'
    aide = "aide.html" if lang == "fr" else f"aide.html#{lang}"
    h = f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t["titre"]}</title>
<meta name="description" content="{t["desc"]}">
<link rel="canonical" href="{url}">
{alt}<meta property="og:type" content="website">
<meta property="og:title" content="{t["titre"]}">
<meta property="og:description" content="{t["desc"]}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="Paperkeep">
<meta property="og:image" content="{BASE}img/capture-detection.png">
<meta name="theme-color" content="#0c2a21">
<link rel="icon" href="img/logo-512.png">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>{CSS}</style>
</head>
<body>

<header class="barre"><div class="w">
  <a class="marque" href="{f}">{LOGO}Paperkeep</a>
  <nav><a href="#fonctionnement">{t["nav"][0]}</a><a href="#confidentialite">{t["nav"][1]}</a><a href="#comptables">{t["nav"][2]}</a><a href="{aide}">{t["nav"][3]}</a></nav>
  <div class="langues">{langues}</div>
  {btn}
</div></header>

<main>
<div class="hero"><div class="w">
  <div>
    <p class="oeil"><i></i>{t["oeil"]}</p>
    <h1><span>{t["h1a"]}</span><span class="b">{t["h1b"]}</span></h1>
    <p class="chapo">{t["chapo"]}</p>
    <div class="actions">{btn}<a class="lien" href="#fonctionnement">{t["voir"]}</a></div>
    <ul class="gages">{"".join(f"<li>{g}</li>" for g in t["gages"])}</ul>
  </div>
  <div class="demo" aria-hidden="true">
    <div class="fenetre">
      <div class="chrome"><i></i><i></i><i></i><b>billing.{v}.example</b><em></em></div>
      <div class="page"><h4>{t["demo_titre"]}</h4>
        {"".join(f'<div class="ligne"><span>{d}</span><span>{m}</span><span class="ok">{t["demo_payee"]}</span></div>' for d, m in lignes)}
      </div>
    </div>
    <div class="bulle"><strong>Paperkeep</strong>
      {"".join(f"<label>{v}<span>{d}</span></label>" for d, _ in lignes)}
      <button tabindex="-1">{t["demo_bouton"]}</button></div>
    <div class="fichiers"><small>{t["demo_dossier"]}</small>{"".join(f"<div>{n}</div>" for n in noms)}</div>
  </div>
</div></div>

<section><div class="w">
  <div class="entete r"><p class="oeil">{t["s1_oeil"]}</p><h2>{t["s1_h"]}</h2><p>{t["s1_p"]}</p></div>
  <div class="avantapres r">
    <div class="pile"><b>{t["avant"]}</b>{"".join(f"<div>{n}</div>" for n in sales)}</div>
    <div class="fleche" aria-hidden="true">→</div>
    <div class="pile propre"><b>{t["apres"]}</b>{"".join(f"<div>{n}</div>" for n in propres)}</div>
  </div>
</div></section>

<section id="fonctionnement" style="padding-top:0"><div class="w">
  <div class="entete r"><p class="oeil">{t["s2_oeil"]}</p><h2>{t["s2_h"]}</h2></div>
  <div class="etapes">{"".join(f'<div class="etape r"><h3>{a}</h3><p>{b}</p></div>' for a, b in t["etapes"])}</div>
  <figure class="capture r"><img src="img/capture-detection.png" width="1280" height="800" loading="lazy" alt="{t["capture_alt"]}"><figcaption>{t["capture_leg"]}</figcaption></figure>
</div></section>

<section style="padding-top:0"><div class="w">
  <div class="entete r"><p class="oeil">{t["s3_oeil"]}</p><h2>{t["s3_h"]}</h2></div>
  <div class="atouts">{"".join(f'<div class="atout r"><svg viewBox="0 0 24 24" aria-hidden="true">{ICONES[i]}</svg><h3>{a}</h3><p>{b}</p></div>' for i, (a, b) in enumerate(t["atouts"]))}</div>
</div></section>

<section class="sombre-s" id="confidentialite"><div class="w">
  <div class="entete r"><p class="oeil">{t["s4_oeil"]}</p><h2>{t["s4_h"]}</h2><p>{t["s4_p"]}</p></div>
  <div class="prive">{"".join(f'<div class="r"><h3>{a}</h3><p>{b}</p></div>' for a, b in t["prive"])}</div>
  <p class="r" style="margin:0;display:flex;flex-wrap:wrap;gap:12px 28px"><a class="lien" href="privacy.html">{t["prive_lien"]}</a><a class="lien" href="{GITHUB}">{t["code_lien"]}</a></p>
</div></section>

<section id="comptables"><div class="w"><div class="compta r">
  <div><p class="oeil">{t["s5_oeil"]}</p><h2>{t["s5_h"]}</h2><p>{t["s5_p"]}</p><a class="btn sombre" href="mailto:{MAIL}">{t["s5_cta"]}</a></div>
  <div class="carte-lien"><b>Chrome Web Store</b>{STORE.replace("https://", "")}</div>
</div></div></section>

<section style="padding-top:0"><div class="w faq">
  <div class="entete r"><h2>{t["faq_h"]}</h2></div>
  {"".join(f'<details class="r"><summary>{q}</summary><p>{r}</p></details>' for q, r in t["faq"])}
  <p class="r" style="margin-top:22px"><a class="lien" href="{aide}">{t["faq_plus"]}</a></p>
</div></section>

<section class="fin"><div class="w r"><h2>{t["fin_h"]}</h2><p>{t["fin_p"]}</p>{btn}</div></section>
</main>

<footer><div class="w">
  <a class="marque" href="{f}" style="color:var(--encre);font-size:17px">{LOGO.replace('width="34" height="34"', 'width="26" height="26"')}Paperkeep</a>
  {"".join(f'<a href="{u}">{n}</a>' for n, u in zip(t["pied"], t["pied_liens"]))}
  <a href="mailto:{MAIL}">{MAIL}</a>
  <p>{t["mention"]}</p>
</div></footer>
<script>{JS}</script>
</body>
</html>
"""
    pathlib.Path(f).write_text(h, encoding="utf-8")
    return f, len(h)


CSS_ARTICLE = r"""
.article{padding-block:64px 90px}.etroit{max-width:760px}
.article h1{font-size:clamp(30px,4.2vw,46px);font-weight:700;margin-bottom:18px}
.article h2{font-size:25px;margin:46px 0 12px}.article h3{font-size:19px;margin:26px 0 8px}
.article p{margin:0 0 16px}.article ul,.article ol{padding-left:22px;margin:0 0 18px}.article li{margin-bottom:8px}
.article a{color:var(--vert);font-weight:550}.article hr{border:0;border-top:1px solid var(--trait);margin:54px 0}
.article code{background:#e6eae6;padding:2px 7px;border-radius:5px;font:500 14.5px/1.5 ui-monospace,Menlo,monospace;overflow-wrap:anywhere}
.article .cta{display:inline-block;margin:10px 0;padding:13px 22px;border-radius:999px;background:var(--vert);color:#fff;font-weight:650;text-decoration:none}
.article .contact{background:var(--papier);border:1px solid var(--trait);border-radius:14px;padding:18px 20px;margin:18px 0}
.article .ancres{font-size:15px}.article .date,.maj{color:var(--gris);font-size:14.5px}
.article details{margin-bottom:8px}
"""

# fichier : (langue, titre, description, type, équivalent dans l'autre langue)
PAGES = {
    "aide.html": ("fr", "Aide et contact — Paperkeep", "Questions fréquentes sur Paperkeep, l'extension Chrome qui récupère vos factures fournisseurs, et comment nous contacter.", "faq", None),
    "guides.html": ("fr", "Guides — récupérer, nommer et transmettre ses factures | Paperkeep", "Guides pratiques pour récupérer, nommer et transmettre ses factures d'achat en ligne à son comptable.", "page", None),
    "guide-factures-abonnements.html": ("fr", "Récupérer les factures de vos abonnements en ligne — guide pratique", "Où trouver les factures de vos abonnements en ligne (logiciels, hébergement, outils) et comment les transmettre proprement à votre comptable.", "article", "gids-facturen-abonnementen.html"),
    "guide-factures-stripe.html": ("fr", "Télécharger toutes ses factures Stripe en une fois (portail client)", "Vos factures d'abonnement sont sur un portail client Stripe ? Où les trouver, comment les télécharger une par une, et comment toutes les récupérer en un clic.", "article", None),
    "guide-nommer-factures.html": ("fr", "Comment nommer ses factures pour son comptable : la convention date, fournisseur, montant", "Une convention simple pour nommer ses factures d'achat : date, fournisseur, montant. Le dossier se trie tout seul et votre comptable s'y retrouve.", "article", None),
    "guide-recu-sans-pdf.html": ("fr", "Pas de facture PDF ? Comment conserver un reçu en ligne pour sa comptabilité", "Certains services en ligne ne fournissent qu'un reçu à l'écran. Trois façons de le conserver proprement et de le transmettre à son comptable.", "article", None),
    "guide-peppol-factures-etrangeres.html": ("fr", "Peppol : les factures de vos abonnements étrangers n'arrivent pas toutes seules", "Depuis 2026, les factures belges arrivent par Peppol. Celles des fournisseurs établis à l'étranger restent des PDF à télécharger : ce que dit la règle et comment s'organiser.", "article", "gids-peppol-buitenlandse-facturen.html"),
    "gids-peppol-buitenlandse-facturen.html": ("nl", "Peppol: de facturen van je buitenlandse abonnementen komen niet vanzelf binnen", "Sinds 2026 komen Belgische facturen via Peppol binnen. Die van buitenlandse leveranciers blijven pdf's om te downloaden: wat de regel zegt en hoe je het aanpakt.", "article", "guide-peppol-factures-etrangeres.html"),
    "gids-facturen-abonnementen.html": ("nl", "De facturen van je online abonnementen terugvinden — praktische gids", "Waar je de facturen van je online abonnementen (software, hosting, tools) vindt en hoe je ze netjes aan je boekhouder bezorgt.", "article", "guide-factures-abonnements.html"),
    "a-propos.html": ("fr", "À propos de Paperkeep — qui édite l'extension", "Paperkeep est une extension Chrome gratuite développée en Belgique. Qui l'édite, pourquoi, et comment nous contacter.", "page", None),
    "privacy.html": ("fr", "Paperkeep — Politique de confidentialité / Privacy policy", "Politique de confidentialité de Paperkeep : aucune donnée n'est envoyée au développeur ni à un tiers.", "page", None),
}
PUBLIE = {"guide-peppol-factures-etrangeres.html": "2026-10-11", "gids-peppol-buitenlandse-facturen.html": "2026-10-11"}
MAJ = {"fr": "Mis à jour le", "nl": "Bijgewerkt op", "en": "Updated on"}


def secondaire(f):
    lang, titre, desc, genre, autre = PAGES[f]
    t = T[lang]
    corps = pathlib.Path("contenu/" + f).read_text(encoding="utf-8")
    url = BASE + f
    alt = ""
    if autre:
        la = PAGES[autre][0]
        alt = f'<link rel="alternate" hreflang="{lang}" href="{url}">\n<link rel="alternate" hreflang="{la}" href="{BASE}{autre}">\n<link rel="alternate" hreflang="x-default" href="{url if lang == "fr" else BASE + autre}">\n'
    ld = [ORGANISATION]
    if genre == "article":
        h1 = re.search(r"<h1>(.*?)</h1>", corps, re.S).group(1)
        ld.append({"@context": "https://schema.org", "@type": "Article", "headline": re.sub("<[^>]+>", "", h1), "description": desc, "inLanguage": lang,
                   "datePublished": PUBLIE.get(f, "2026-10-09"), "dateModified": AUJOURDHUI, "mainEntityOfPage": url, "image": BASE + "img/capture-detection.png",
                   "author": {"@id": BASE + "#organisation"}, "publisher": {"@id": BASE + "#organisation"}})
        corps = corps.replace("</h1>", f'</h1>\n  <p class="maj">{MAJ[lang]} {AUJOURDHUI} · Paperkeep</p>', 1)
    if genre == "faq":
        bloc = corps.split('<h2 id="en">')[0]
        qa = re.findall(r"<summary>(.*?)</summary><p>(.*?)</p>", bloc, re.S)
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "dateModified": AUJOURDHUI,
                   "mainEntity": [{"@type": "Question", "name": re.sub("<[^>]+>", "", q), "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", r)}} for q, r in qa]})
    accueil = FICHIER[lang]
    aide = "aide.html" if lang == "fr" else f"aide.html#{lang}"
    courant = ' aria-current="true"'
    langues = "".join(f'<a href="{FICHIER[l]}"{courant if l == lang else ""} lang="{l}">{l.upper()}</a>' for l in ("fr", "nl", "en"))
    h = f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titre}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
{alt}<meta property="og:type" content="{"article" if genre == "article" else "website"}">
<meta property="og:title" content="{titre}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="Paperkeep">
<meta property="og:image" content="{BASE}img/capture-detection.png">
<meta name="theme-color" content="#0c2a21">
<link rel="icon" href="img/logo-512.png">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>{CSS}{CSS_ARTICLE}</style>
</head>
<body>
<header class="barre"><div class="w">
  <a class="marque" href="{accueil}">{LOGO}Paperkeep</a>
  <nav><a href="{accueil}#fonctionnement">{t["nav"][0]}</a><a href="{accueil}#confidentialite">{t["nav"][1]}</a><a href="{accueil}#comptables">{t["nav"][2]}</a><a href="{aide}">{t["nav"][3]}</a></nav>
  <div class="langues">{langues}</div>
  <a class="btn" href="{STORE}">{CHROME_ICO}{t["cta"]} <small>— {t["cta_sub"]}</small></a>
</div></header>
<main class="article"><div class="w etroit">
{corps}
</div></main>
<footer><div class="w">
  <a class="marque" href="{accueil}" style="color:var(--encre);font-size:17px">{LOGO.replace('width="34" height="34"', 'width="26" height="26"')}Paperkeep</a>
  {"".join(f'<a href="{u}">{n}</a>' for n, u in zip(t["pied"], t["pied_liens"]))}
  <a href="mailto:{MAIL}">{MAIL}</a>
  <p>{t["mention"]}</p>
</div></footer>
</body>
</html>
"""
    pathlib.Path(f).write_text(h, encoding="utf-8")
    return f, len(h)


def plan_du_site():
    urls = [""] + ["en.html", "nl.html"] + list(PAGES)
    x = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    x += "".join(f"  <url><loc>{BASE}{u}</loc><lastmod>{AUJOURDHUI}</lastmod></url>\n" for u in urls) + "</urlset>\n"
    pathlib.Path("sitemap.xml").write_text(x, encoding="utf-8")
    return urls


if __name__ == "__main__":
    for lang in T:
        print(*page(lang))
    for f in PAGES:
        print(*secondaire(f))
    print("plan du site :", len(plan_du_site()), "adresses")
