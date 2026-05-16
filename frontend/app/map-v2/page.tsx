import { redirect } from "next/navigation";

/**
 * /map-v2 is kept as a permanent redirect stub so existing bookmarks
 * and external links continue to resolve.  The canonical route is /map.
 */
export default function MapV2Page() {
  redirect("/map");
}
