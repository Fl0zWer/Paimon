/**
 * All Levels
 * Complete list of all level submissions.
 * Now uses the unified level schema for consistency.
 */

import { normalizeLevel } from './levelSchema.js';

// Raw level data from various sources
const rawLevels = [
  {
    "id": "118509879",
    "name": "Skeletal Shenanigans",
    "creator": "YoReid",
    "difficulty": "Medium Demon",
    "stars": "10",
    "downloads": "16665671",
    "likes": "959350",
    "song": "Slash Inferno",
    "length": "XL",
    "url": "https://gdbrowser.com/118509879",
    "requested_by": {
      "user_id": 672496337006362634,
      "username": "flozwer",
      "display_name": "FlozWer"
    },
    "requested_at": "2025-06-30T15:45:57.196096",
    "server_id": 1215038551755067442,
    "server_name": "𝐏𝐚𝐢𝐦𝐨𝐧𝐋𝐚𝐧𝐝𝐢𝐚"
  },
  {
    "id": "116791791",
    "name": "GD GANGSTER RAP",
    "creator": "BoomKitty",
    "difficulty": "Insano",
    "stars": "8",
    "downloads": "8265184",
    "likes": "453667",
    "song": "GEOMETRY DASH GANGSTER RAP",
    "length": "XL",
    "url": "https://gdbrowser.com/116791791",
    "requested_by": {
      "user_id": 672496337006362634,
      "username": "flozwer",
      "display_name": "FlozWer",
      "platform": "Discord"
    },
    "requested_at": "2025-07-02T17:02:42.676473",
    "server_id": 1215038551755067442,
    "server_name": "𝐏𝐚𝐢𝐦𝐨𝐧𝐋𝐚𝐧𝐝𝐢𝐚",
    "platform": "Discord",
    "all_levels_unique_id": 2
  },
  {
    "id": "120512937",
    "nombre": "Wazaaaa",
    "creador": "FlozWer",
    "dificultad": "Más Difícil",
    "estrellas": "0",
    "downloads": "580",
    "likes": "48",
    "length": "Long",
    "song_name": "1991 REEBOK PUMPS (demo)",
    "song_artist": "SpeedoSausage",
    "url": "https://gdbrowser.com/120512937",
    "image_url": null,
    "description": "porfin arregle el problema del unlisted 8)",
    "version": 1,
    "uploaded": "",
    "updated": "",
    "original": 0,
    "two_player": false,
    "ldm": false,
    "epic": false,
    "featured": false,
    "auto": false,
    "demon": false,
    "coins": 0,
    "verified_coins": false,
    "requested_stars": 0,
    "orbs": "N/A",
    "song_id": "759834",
    "song_size": "N/A",
    "discord_user_id": "672496337006362634",
    "showcase_video": null,
    "moderator_note": null,
    "submitted_via": "modal_form",
    "request_id": "REQ4929530QWN",
    "submitted_by": "FlozWer",
    "submitted_by_id": "672496337006362634",
    "submission_timestamp": "2025-07-02T21:49:13.088932",
    "all_levels_unique_id": 5
  },
  {
    "id": "112",
    "name": "Level Search",
    "creator": "Desconocido",
    "difficulty": "Desconocido",
    "stars": "N/A",
    "downloads": "N/A",
    "likes": "N/A",
    "song": "",
    "length": "N/A",
    "url": "https://gdbrowser.com/112",
    "requested_by": {
      "user_id": 672496337006362634,
      "username": "flozwer",
      "display_name": "FlozWer",
      "platform": "Discord"
    },
    "requested_at": "2025-07-07T12:12:38.851969",
    "server_id": 1215038551755067442,
    "server_name": "𝐏𝐚𝐢𝐦𝐨𝐧𝐋𝐚𝐧𝐝𝐢𝐚",
    "platform": "Discord",
    "all_levels_unique_id": 6
  }
];

// Export normalized levels
export const levels = rawLevels.map(level => normalizeLevel(level));