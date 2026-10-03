def padding_length(data):

    block_size = 16

    remainder = len(data) % block_size

    padding = block_size - remainder

    return padding  
