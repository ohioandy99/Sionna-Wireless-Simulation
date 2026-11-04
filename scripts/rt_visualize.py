from pathlib import Path
import sionna.rt
from sionna.rt import load_scene, PlanarArray, Transmitter, Receiver, Camera, PathSolver

def main():
    # 1) Load an integrated scene (built-in)
    # Docs show examples like munich, etoile, simple_street_canyon
    scene = load_scene(sionna.rt.scene.munich, merge_shapes=True)  # faster with merge_shapes=True
    scene.frequency = 28e9  # 28 GHz (you can change)

    # 2) Define antenna arrays for Tx/Rx (simple 1x1 isotropic-like patterns)
    scene.tx_array = PlanarArray(num_rows=1, num_cols=1,
                                 vertical_spacing=0.5, horizontal_spacing=0.5,
                                 pattern="tr38901", polarization="V")
    scene.rx_array = PlanarArray(num_rows=1, num_cols=1,
                                 vertical_spacing=0.5, horizontal_spacing=0.5,
                                 pattern="dipole", polarization="V")

    # 3) Add a transmitter (UE) and a receiver (BS)
    tx = Transmitter(name="UE", position=[8.5, 21, 1.5], display_radius=2)
    rx = Receiver(name="BS", position=[45, 90, 10.0], display_radius=2)
    scene.add(tx)
    scene.add(rx)

    # Make UE "look at" BS (only affects antenna orientation)
    tx.look_at(rx)

    # 4) Ray tracing: compute propagation paths
    p_solver = PathSolver()
    paths = p_solver(scene=scene,
                     max_depth=3,
                     los=True,
                     specular_reflection=True,
                     diffuse_reflection=False,
                     refraction=True,
                     synthetic_array=False,
                     seed=1)

    # 5) Visualize
    # Option A) interactive preview (Jupyter only)
    # scene.preview(paths=paths, clip_at=30)

    # Option B) render to file (works in normal python script)
    cam = Camera(position=[-250, 250, 150], look_at=[-15, 30, 28])
    scene.render_to_file(camera=cam,
                         paths=paths,
                         filename=str(Path(__file__).resolve().parent.parent / "figures" / "rt_paths_script.png"),
                         resolution=[900, 650],
                         num_samples=256,
                         clip_at=30)

    print("Saved: figures/rt_paths_script.png")

if __name__ == "__main__":
    main()
