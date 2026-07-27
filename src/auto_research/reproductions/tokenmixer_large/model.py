from ..rankmixer.model import RankMixerConfig, build_model, train_model


def build_tokenmixer_large(data, config):
    """Paper-faithful TokenMixer-Large block already shared with evolve RankMixer."""
    return build_model("tokenmixer_large", data, config)
