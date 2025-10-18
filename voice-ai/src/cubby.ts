// src/lib/cubby.ts
import { createClient } from "@cubby/js";

export const cubby = createClient({
  baseUrl: "https://api.cubby.sh",
  clientId: process.env.CUBBY_CLIENT_ID!,
  clientSecret: process.env.CUBBY_CLIENT_SECRET!,
});
