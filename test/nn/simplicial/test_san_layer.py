"""Test the SAN layer."""
import torch

from topomodelx.nn.simplicial.san_layer import SANLayer


class TestSANLayer:
    """Unit tests for the SANLayer class."""

    def test_forward(self):
        """Test the forward method of SANLayer."""
        in_channels = 2
        out_channels = 5
        n_filters = [1, 2, 3]

        for num_filters_j in n_filters:
            san_layer = SANLayer(in_channels, out_channels, n_filters=num_filters_j)

            # Create input tensors
            n_cells = 100
            x = torch.randn(n_cells, in_channels)
            laplacian_up = torch.sparse_coo_tensor(
                indices=torch.tensor([[0, 1, 2], [1, 2, 0]]),
                values=torch.tensor([0.5, 0.3, 0.2]),
                size=(n_cells, n_cells),
            )
            laplacian_down = torch.sparse_coo_tensor(
                indices=torch.tensor([[0, 1, 2], [1, 2, 0]]),
                values=torch.tensor([0.3, 0.4, 0.5]),
                size=(n_cells, n_cells),
            )
            P = torch.randn(n_cells, n_cells)

            # Perform forward pass
            output = san_layer(x, laplacian_up, laplacian_down, P)
            assert output.shape == (n_cells, out_channels)

    def test_reset_parameters(self):
        """Test the reset_parameters method of SANLayer."""
        in_channels = 2
        out_channels = 5
        n_filters = 2

        san_layer = SANLayer(
            in_channels=in_channels,
            out_channels=out_channels,
            n_filters=n_filters,
        )
        san_layer.reset_parameters()

        for module in san_layer.modules():
            if hasattr(module, "reset_parameters"):
                module.reset_parameters()
