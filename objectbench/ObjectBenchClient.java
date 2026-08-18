package bench;

import java.nio.file.*;
import java.util.*;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import net.fabricmc.fabric.api.client.rendering.v1.level.LevelRenderEvents;
import net.fabricmc.loader.api.FabricLoader;

public final class ObjectBenchClient implements ClientModInitializer {
    static final String[] NAMES = {"geometry_transparency", "occlusion_entities", "mixed_block_entities"};
    static final double[][] START = {{-36,12,-40}, {124,11,-40}, {284,12,-40}};
    static final double[][] END   = {{ 36,12,-40}, {196,11,-40}, {356,12,-40}};

    static long envMs(String key, long def) {
        try { return Long.parseLong(System.getenv().getOrDefault(key, Long.toString(def))); }
        catch (Exception ignored) { return def; }
    }

    static final long INITIAL = envMs("BENCH_INITIAL_MS", 8000) * 1_000_000L;
    static final long WARM    = envMs("BENCH_WARM_MS", 3000) * 1_000_000L;
    static final long MEASURE = envMs("BENCH_MEASURE_MS", 8000) * 1_000_000L;
    static final long SCENE   = WARM + MEASURE;

    @SuppressWarnings("unchecked")
    static final List<Long>[] S = new List[]{new ArrayList<>(), new ArrayList<>(), new ArrayList<>()};
    static final List<Long> ALL = new ArrayList<>();
    static long boot = 0, lastFrame = 0;
    static boolean done = false;
    static Path out;
    static String run;

    @Override
    public void onInitializeClient() {
        out = FabricLoader.getInstance().getGameDir().resolve("objectbench-result.json");
        run = System.getenv().getOrDefault("BENCH_RUN", "unknown");
        try { Files.deleteIfExists(out); } catch (Exception ignored) {}

        ClientTickEvents.END_CLIENT_TICK.register(client -> {
            if (done || client.player == null || client.level == null) return;
            long now = System.nanoTime();
            if (boot == 0) {
                boot = now;
                System.out.println("OBJECTBENCH WORLD READY " + run);
                return;
            }

            long elapsed = now - boot;
            if (elapsed < INITIAL) return;
            long q = elapsed - INITIAL;
            int scene = (int)(q / SCENE);
            if (scene >= NAMES.length) {
                done = true;
                write();
                return;
            }

            long within = q % SCENE;
            double p = Math.min(1.0, within / (double)SCENE);
            double x = START[scene][0] + (END[scene][0] - START[scene][0]) * p;
            client.player.setPos(x, START[scene][1], START[scene][2]);
            client.player.setYRot((float)(Math.sin(p * Math.PI * 2.0) * 7.0));
            client.player.setXRot(-3.0f);
        });

        LevelRenderEvents.END_MAIN.register(ctx -> frame());
        System.out.println("OBJECTBENCH READY " + run);
    }

    static void frame() {
        long now = System.nanoTime();
        if (lastFrame == 0) { lastFrame = now; return; }
        long dt = now - lastFrame;
        lastFrame = now;
        if (done || boot == 0 || dt <= 0 || dt >= 2_000_000_000L) return;

        long elapsed = now - boot;
        if (elapsed < INITIAL) return;
        long q = elapsed - INITIAL;
        int scene = (int)(q / SCENE);
        if (scene < 0 || scene >= NAMES.length) return;
        long within = q % SCENE;
        if (within >= WARM) {
            S[scene].add(dt);
            ALL.add(dt);
        }
    }

    static Map<String,Object> metric(List<Long> in) {
        Map<String,Object> m = new LinkedHashMap<>();
        if (in.isEmpty()) { m.put("samples", 0); return m; }
        List<Long> x = new ArrayList<>(in);
        Collections.sort(x);
        long sum = 0;
        for (long v : in) sum += v;
        m.put("samples", in.size());
        m.put("mean_fps", in.size() * 1e9 / sum);
        m.put("median_fps", 1e9 / percentile(x, .5));
        m.put("one_percent_low_fps", 1e9 / percentile(x, .99));
        m.put("zero_point_one_percent_low_fps", 1e9 / percentile(x, .999));
        m.put("p99_frame_ms", percentile(x, .99) / 1e6);
        return m;
    }

    static long percentile(List<Long> x, double q) {
        int i = (int)Math.ceil(q * x.size()) - 1;
        return x.get(Math.max(0, Math.min(x.size() - 1, i)));
    }

    static String num(Object o) {
        return o instanceof Number ? String.format(Locale.ROOT, "%.5f", ((Number)o).doubleValue()) : "0";
    }

    static String metricJson(Map<String,Object> m) {
        return String.format(Locale.ROOT,
            "{\"samples\":%d,\"mean_fps\":%s,\"median_fps\":%s,\"one_percent_low_fps\":%s,\"zero_point_one_percent_low_fps\":%s,\"p99_frame_ms\":%s}",
            ((Number)m.getOrDefault("samples", 0)).intValue(),
            num(m.get("mean_fps")), num(m.get("median_fps")), num(m.get("one_percent_low_fps")),
            num(m.get("zero_point_one_percent_low_fps")), num(m.get("p99_frame_ms")));
    }

    static void write() {
        try {
            StringBuilder b = new StringBuilder();
            b.append("{\"run\":\"").append(run).append("\",\"overall\":").append(metricJson(metric(ALL))).append(",\"scenes\":{");
            for (int i = 0; i < NAMES.length; i++) {
                if (i > 0) b.append(',');
                b.append('\"').append(NAMES[i]).append("\":").append(metricJson(metric(S[i])));
            }
            b.append("}}\n");
            Files.writeString(out, b.toString());
            System.out.println("OBJECTBENCH DONE " + b);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
