from unittest.mock import MagicMock, patch

import pytest

from registest.core.pipeline import Pipeline


@pytest.fixture
def mock_data_manager():
    """
    Fixture to create a mock DataManager.
    """
    mock_dm = MagicMock()
    mock_dm.ref.data = "mock_reference_image"
    return mock_dm


@pytest.fixture
def mock_parameters():
    """
    Fixture to create a mock Parameters object.
    """
    return MagicMock(prepare={"shifts": [[0, 0, 0], [1, 1, 1]]})


@pytest.fixture
def mock_transform():
    """
    Fixture to create a mock Transform object.
    """
    with patch(
        "registest.core.pipeline.Transform", autospec=True
    ) as mock_transform_class:
        mock_transform_instance = mock_transform_class.return_value
        mock_transform_instance.execute.return_value = "mock_transformed_image"
        yield mock_transform_instance


def test_pipeline_initialization(mock_data_manager, mock_parameters):
    """
    Test Pipeline initialization.
    """
    pipeline = Pipeline(
        datam=mock_data_manager, params=mock_parameters, raw_cmd_list="prepare"
    )
    assert pipeline.datam == mock_data_manager
    assert pipeline.params == mock_parameters
    assert pipeline.ref == "mock_reference_image"
    assert pipeline.target_nbr == len(mock_parameters.prepare["shifts"])


@patch("registest.core.pipeline.Transform", autospec=True)
def test_pipeline_prepare(
    mock_transform_class,
    mock_data_manager,
    mock_parameters,
):
    """
    Test the prepare method in the Pipeline class.
    """

    # Mock the Transform instance
    mock_transform_instance = mock_transform_class.return_value
    mock_transform_instance.execute.return_value = "mock_transformed_image"

    pipeline = Pipeline(
        datam=mock_data_manager, params=mock_parameters, raw_cmd_list="prepare"
    )
    pipeline.prepare()

    # Verify that Transform was initialized with the correct parameters
    mock_transform_class.assert_called_once_with(mock_parameters.prepare)

    # Verify that execute was called for each target
    assert mock_transform_instance.execute.call_count == len(
        mock_parameters.prepare["shifts"]
    )
    for i in range(len(mock_parameters.prepare["shifts"])):
        mock_transform_instance.execute.assert_any_call("mock_reference_image", i)

    # Verify that DataManager.save_tif was called with the correct arguments
    assert mock_data_manager.save_tif.call_count == len(
        mock_parameters.prepare["shifts"]
    )
    for i in range(len(mock_parameters.prepare["shifts"])):
        mock_data_manager.save_tif.assert_any_call(
            data="mock_transformed_image", folder="Preparation", name=f"target_{i}"
        )
