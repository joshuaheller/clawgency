# Clawgency – Website-Handbuch & README

Herzlichen Glückwunsch zu Ihrer neuen Website-Vorlage für Clawgency! Dieses Dokument dient als Handbuch, um Ihnen den Einstieg, die Anpassung und die Bereitstellung Ihrer neuen Landing Page zu erleichtern.

## Projektübersicht

Das Projekt ist eine statische Website, die mit reinem HTML, CSS und JavaScript erstellt wurde. Es gibt keine komplexen Build-Schritte oder Framework-Abhängigkeiten, was die Bearbeitung und das Hosting extrem einfach macht.

### Dateistruktur

```
/clawgency
├── 📂 assets/          (Platzhalter für Bilder, Logos etc.)
├── 📄 index.html       (Die Haupt-Landing-Page)
├── 📄 styles.css       (Alle Stile für das Design und die Animationen)
├── 📄 script.js        (Alle Interaktionen und Animationen)
├── 📄 datenschutz.html (Vorlage für die Datenschutzerklärung)
├── 📄 agb.html         (Vorlage für die AGB)
└── 📄 README.md        (Dieses Handbuch)
```

## Erste Schritte & Anpassungen

Sie können dieses Projekt direkt in einem Code-Editor wie **Cursor**, VS Code oder Sublime Text öffnen und bearbeiten.

### 1. Inhalte anpassen (`index.html`)

Öffnen Sie die `index.html`. Der gesamte Text ist direkt im HTML-Code als Klartext hinterlegt. Suchen Sie einfach nach dem Text, den Sie ändern möchten, und ersetzen Sie ihn.

**Wichtige Bereiche zur Anpassung:**

- **SEO & Meta-Tags (im `<head>`-Bereich):**
  - `<title>`: Der Titel, der im Browser-Tab angezeigt wird.
  - `<meta name="description">`: Die Beschreibung für Suchmaschinen.
  - `<meta name="keywords">`: Die Keywords für Suchmaschinen.
  - **Open Graph & Twitter Cards:** Passen Sie die `og:...` und `twitter:...` Tags an, um das Erscheinungsbild beim Teilen auf sozialen Medien zu steuern. Erstellen Sie ein Vorschaubild (`og-image.png`) und laden Sie es hoch.

- **Kontaktformular (im `<section id="kontakt">`-Bereich):**
  - Das Formular ist derzeit nur eine visuelle Vorlage. Um es funktionsfähig zu machen, müssen Sie den `submit`-Event in `script.js` an einen Backend-Dienst wie Formspree, Netlify Forms oder einen eigenen E-Mail-Versand-Endpunkt anbinden.

- **Footer-Links:**
  - Passen Sie die Links im Footer an, insbesondere den Link zum Impressum auf Ihrer Hauptseite `theaisoftwarecompany.com`.

### 2. Design anpassen (`styles.css`)

Öffnen Sie die `styles.css`. Am Anfang der Datei finden Sie einen `:root`-Block, der alle zentralen Design-Variablen enthält.

```css
:root {
  /* Farben */
  --c-bg:         #0a0d14;       /* Hintergrund */
  --c-accent:     #00e5ff;       /* Akzentfarbe (Türkis) */
  --c-text:       #e8eaf0;       /* Haupttextfarbe */
  --c-text-muted: #8892a4;       /* Gedämpfte Textfarbe */

  /* Schriftarten */
  --f-heading: 'Syne', sans-serif;
  --f-body:    'Space Grotesk', sans-serif;
}
```

- **Farben ändern:** Ändern Sie einfach die Hex-Codes in diesem Block, um das gesamte Farbschema der Website anzupassen.
- **Schriftarten ändern:** Die Schriftarten (`Syne` und `Space Grotesk`) werden von Google Fonts geladen. Sie können sie in `index.html` (im `<head>`) durch andere Schriftarten ersetzen und die Namen hier in den CSS-Variablen aktualisieren.

### 3. Rechtliche Texte (`datenschutz.html`, `agb.html`)

Die bereitgestellten Dateien sind **nur Vorlagen**. Sie müssen diese unbedingt mit Ihren eigenen, rechtlich geprüften Inhalten füllen. Insbesondere das Impressum muss vollständig und korrekt sein. Es wird empfohlen, hierfür einen Anwalt oder einen spezialisierten Online-Dienst zu konsultieren.

## Bereitstellung (Deployment)

Da es sich um eine rein statische Website handelt, ist das Hosting sehr einfach und kostengünstig. Sie können die Dateien einfach per FTP auf einen beliebigen Webspace hochladen oder einen der folgenden modernen Hosting-Anbieter nutzen:

- **Vercel:** Verbinden Sie ein GitHub-Repository. Vercel erkennt das Projekt automatisch und stellt es bereit. Ideal für schnelle, globale Ladezeiten.
- **Netlify:** Ähnlich wie Vercel, ebenfalls mit hervorragender kostenloser Stufe.
- **GitHub Pages:** Kostenloses Hosting direkt aus Ihrem GitHub-Repository.

**Typischer Workflow mit Vercel/Netlify:**

1.  Erstellen Sie ein neues, privates Repository auf GitHub.
2.  Laden Sie alle Projektdateien in dieses Repository hoch.
3.  Erstellen Sie ein Konto bei Vercel oder Netlify und verbinden Sie es mit Ihrem GitHub-Konto.
4.  Wählen Sie das soeben erstellte Repository aus.
5.  Die Plattform erkennt, dass es sich um ein statisches Projekt handelt, und stellt es mit einem Klick bereit.
6.  Weisen Sie Ihre Domain `clawgency.de` in den Einstellungen der Plattform zu.

## Zusammenfassung

Dieses Projekt ist darauf ausgelegt, Ihnen maximale kreative Freiheit bei minimalem technischen Aufwand zu geben. Mit grundlegenden HTML- und CSS-Kenntnissen können Sie jeden Aspekt dieser Seite an Ihre Marke anpassen.

Viel Erfolg mit Clawgency!
