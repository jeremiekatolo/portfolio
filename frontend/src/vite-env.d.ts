/// <reference types="vite/client" />

/**
 * Déclarations de types pour Vite.
 *
 * Le triple-slash reference ci-dessus charge les types Vite par défaut :
 * - import.meta.env (VITE_*)
 * - import de fichiers .css, .svg, .png, etc.
 *
 * Sans ce fichier, TypeScript refuse les imports CSS et l'accès à
 * import.meta.env.
 */

interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}