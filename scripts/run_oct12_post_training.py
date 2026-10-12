"""Execute bounded real-checkpoint October 9 post-training mechanisms."""
import argparse
from pathlib import Path
from auto_research.post_training.oct12_checkpoint import OBJECTIVES, normalize_objective, run_checkpoint


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--objective",type=normalize_objective,choices=OBJECTIVES,required=True,
                        help="canonical paper key; cast is a compatibility alias for cast-opd")
    for role in ("student","teacher","auxiliary","expert","analyzer"):
        parser.add_argument(f"--{role}-path",type=Path,required=role in {"student","teacher"})
        parser.add_argument(f"--{role}-id",required=role in {"student","teacher"})
        parser.add_argument(f"--{role}-revision",required=role in {"student","teacher"})
    for name in ("train-path","validation-path","split-manifest","output"):
        parser.add_argument(f"--{name}",type=Path,required=True)
    parser.add_argument("--dataset-revision",required=True)
    parser.add_argument("--device",default="cuda")
    defaults = {"seed":42,"steps":2,"max-tokens":64,"group":2,"validation-examples":4,
        "forks":3,"continuations":2,"min-fork-gap":1,"credit-size":6,"priming-examples":2,
        "rounds":2,"pool-examples":4,"acquisition":2,"replay-quota":1,"teacher-rollouts":2,"analyzer-tokens":256}
    for name,default in defaults.items():
        parser.add_argument(f"--{name}",type=int,default=default)
    for name,default in {"learning-rate":1e-5,"pbr-weight":1.,"kl-weight":.01,"retention":.6}.items():
        parser.add_argument(f"--{name}",type=float,default=default)
    run_checkpoint(**vars(parser.parse_args(argv)))


if __name__=="__main__":
    main()
