import "dotenv/config";
import { createClient } from "@cubby/js";

const cubby = createClient({
  baseUrl: "https://api.cubby.sh",
  clientId: process.env.CUBBY_CLIENT_ID,
  clientSecret: process.env.CUBBY_CLIENT_SECRET,
});

const run = async () => {
  const { devices } = await cubby.listDevices();
  console.log(
    "Devices:",
    devices?.map((d) => ({ id: d.id, name: d.name }))
  );
  if (devices?.[0]) {
    cubby.setDeviceId(devices[0].id);
    const r = await cubby.search({ q: "hello", content_type: "ocr", limit: 1 });
    console.log("Search OK (sample):", r?.results?.length ?? 0);
  }
};
run().catch((e) => {
  console.error(e);
  process.exit(1);
});
