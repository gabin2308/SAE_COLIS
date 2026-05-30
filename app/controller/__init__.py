import os
import glob
import importlib

# Chaque controller doit exposer : ctrl = MonController()
def register_all(app, url_prefix="/api"):
    folder = os.path.dirname(__file__)
    files  = glob.glob(folder + "/*.py")

    for f in files:
        module_name = os.path.basename(f)[:-3]
        if module_name.startswith("_"):
            continue  # ignore __init__.py

        module = importlib.import_module(f"app.controller.{module_name}")

        if hasattr(module, "ctrl"):
            # Convention : le nom du blueprint = préfixe URL
            name   = module.ctrl.blueprint.name
            prefix = f"{url_prefix}/{name}"
            app.register_blueprint(module.ctrl.blueprint, url_prefix=prefix)
            print(f"[OK] Blueprint '{name}' enregistré sur {prefix}")