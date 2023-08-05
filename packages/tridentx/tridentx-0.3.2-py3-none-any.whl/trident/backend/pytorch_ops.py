import os
import sys
from typing import Tuple, Optional, Union
from collections import Sized, Iterable
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from functools import partial
import numpy as np
from .common import get_session,addindent,get_time_suffix,get_class,PrintException
_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
__all__ = ['argmax','reduce_max','reduce_min','reduce_mean','reduce_sum','expand_dims','meshgrid','element_cosine_distance','gram_matrix','get_rotation_matrix2d','warp_affine']


def argmax(t:torch.Tensor,axis=1):
    _, idx = t.max(dim=axis)
    return idx


def reduce_mean(t:torch.Tensor,axis=1,keepdim=False):
    return t.mean(dim=axis,keepdim=keepdim)
def reduce_sum(t:torch.Tensor,axis=1,keepdim=False):
    return t.sum(dim=axis,keepdim=keepdim)

def reduce_max(t:torch.Tensor,axis=1,keepdim=False):
    arr, idx = t.max(dim=axis,keepdim=keepdim)
    return arr

def reduce_min(t:torch.Tensor,axis=1,keepdim=False):
    arr, idx = t.min(dim=axis,keepdim=keepdim)
    return arr

def expand_dims(t:torch.Tensor,axis=0):
    return t.unsqueeze(axis)


def element_cosine_distance(v1, v2, axis=-1):
    reduce_dim = -1
    cos = (v1 * v2).sum(dim=reduce_dim,keepdims=False) /((v1 * v1).sum(dim=reduce_dim, keepdims=False).sqrt()*(v2 * v2).sum(dim=reduce_dim, keepdims=False).sqrt())
    return cos







def torch_rot90_(x: torch.Tensor):
    return x.transpose_(2, 3).flip(2)


def torch_rot90(x: torch.Tensor):
    return x.transpose(2, 3).flip(2)


def torch_rot180(x: torch.Tensor):
    return x.flip(2).flip(3)


def torch_rot270(x: torch.Tensor):
    return x.transpose(2, 3).flip(3)


def torch_flipud(x: torch.Tensor):
    """
    Flip image tensor vertically
    :param x:
    :return:
    """
    return x.flip(2)


def torch_fliplr(x: torch.Tensor):
    """
    Flip image tensor horizontally
    :param x:
    :return:
    """
    return x.flip(3)






def pad_image_tensor(image_tensor: torch.Tensor, pad_size: int = 32):
    """Pad input tensor to make it's height and width dividable by @pad_size

    :param image_tensor: Input tensor of shape NCHW
    :param pad_size: Pad size
    :return: Tuple of output tensor and pad params. Second argument can be used to reverse pad operation of model output
    """
    rows, cols = image_tensor.size(2), image_tensor.size(3)
    if (
        isinstance(pad_size, Sized)
        and isinstance(pad_size, Iterable)
        and len(pad_size) == 2
    ):
        pad_height, pad_width = [int(val) for val in pad_size]
    elif isinstance(pad_size, int):
        pad_height = pad_width = pad_size
    else:
        raise ValueError(
            "Unsupported pad_size: {pad_size}, must be either tuple(pad_rows,pad_cols) or single int scalar."
        )

    if rows > pad_height:
        pad_rows = rows % pad_height
        pad_rows = pad_height - pad_rows if pad_rows > 0 else 0
    else:
        pad_rows = pad_height - rows

    if cols > pad_width:
        pad_cols = cols % pad_width
        pad_cols = pad_width - pad_cols if pad_cols > 0 else 0
    else:
        pad_cols = pad_width - cols

    if pad_rows == 0 and pad_cols == 0:
        return image_tensor, (0, 0, 0, 0)

    pad_top = pad_rows // 2
    pad_btm = pad_rows - pad_top

    pad_left = pad_cols // 2
    pad_right = pad_cols - pad_left

    pad = [pad_left, pad_right, pad_top, pad_btm]
    image_tensor = torch.nn.functional.pad(image_tensor, pad)
    return image_tensor, pad


def unpad_image_tensor(image_tensor, pad):
    pad_left, pad_right, pad_top, pad_btm = pad
    rows, cols = image_tensor.size(2), image_tensor.size(3)
    return image_tensor[..., pad_top : rows - pad_btm, pad_left : cols - pad_right]


def unpad_xyxy_bboxes(bboxes_tensor: torch.Tensor, pad, dim=-1):
    pad_left, pad_right, pad_top, pad_btm = pad
    pad = torch.tensor(
        [pad_left, pad_top, pad_left, pad_top], dtype=bboxes_tensor.dtype
    ).to(bboxes_tensor.device)

    if dim == -1:
        dim = len(bboxes_tensor.size()) - 1

    expand_dims = list(set(range(len(bboxes_tensor.size()))) - {dim})
    for i, dim in enumerate(expand_dims):
        pad = pad.unsqueeze(dim)

    return bboxes_tensor - pad




def meshgrid(x, y, normalized_coordinates=True):
    '''Return meshgrid in range x & y.

    Args:
      x: (int) first dim range.
      y: (int) second dim range.
      row_major: (bool) row major or column major.

    Returns:
      (tensor) meshgrid, sized [x*y,2]

    Example:
    >> meshgrid(3,2)
    0  0
    1  0
    2  0
    0  1
    1  1
    2  1
    [torch.FloatTensor of size 6x2]

    >> meshgrid(3,2,row_major=False)
    0  0
    0  1
    0  2
    1  0
    1  1
    1  2
    [torch.FloatTensor of size 6x2]
    '''
    xs = torch.linspace(0, x - 1, x, device=_device, dtype=torch.float)
    ys = torch.linspace(0, y - 1, y, device=_device, dtype=torch.float)
    if normalized_coordinates:
        xs = torch.linspace(-1, 1, x, device=_device, dtype=torch.float)
        ys = torch.linspace(-1, 1, y, device=_device, dtype=torch.float)


    base_grid=torch.stack(torch.meshgrid([xs, ys])).transpose(1, 2)
    return torch.unsqueeze(base_grid, dim=0).permute(0, 2, 3, 1)


def gram_matrix(input):
    a, b, c, d = input.size()  # a=batch size(=1)
    # b=number of feature maps
    # (c,d)=dimensions of a f. map (N=c*d)
    features = input.view(a * b, c * d)  # resise F_XL into \hat F_XL
    G = torch.mm(features, features.t())  # compute the gram product
    return G


def angle_to_rotation_matrix(angle) -> torch.Tensor:
    """
    Creates a rotation matrix out of angles in degrees
    Args:
        angle: (torch.Tensor): tensor of angles in degrees, any shape.

    Returns:
        torch.Tensor: tensor of *x2x2 rotation matrices.

    Shape:
        - Input: :math:`(*)`
        - Output: :math:`(*, 2, 2)`

    Example:
        >>> input = torch.rand(1, 3)  # Nx3
        >>> output = angle_to_rotation_matrix(input)  # Nx3x2x2
    """
    ang_rad =angle*np.pi/180
    cos_a= torch.cos(ang_rad)
    sin_a= torch.sin(ang_rad)
    return torch.stack([cos_a, sin_a, -sin_a, cos_a], dim=-1).view(*angle.shape, 2, 2)


def get_rotation_matrix2d(
        center: torch.Tensor,
        angle,
        scale) -> torch.Tensor:
    r"""Calculates an affine matrix of 2D rotation.

    The function calculates the following matrix:

    .. math::
        \begin{bmatrix}
            \alpha & \beta & (1 - \alpha) \cdot \text{x}
            - \beta \cdot \text{y} \\
            -\beta & \alpha & \beta \cdot \text{x}
            + (1 - \alpha) \cdot \text{y}
        \end{bmatrix}

    where

    .. math::
        \alpha = \text{scale} \cdot cos(\text{angle}) \\
        \beta = \text{scale} \cdot sin(\text{angle})

    The transformation maps the rotation center to itself
    If this is not the target, adjust the shift.

    Args:
        center (Tensor): center of the rotation in the source image.
        angle (Tensor): rotation angle in degrees. Positive values mean
            counter-clockwise rotation (the coordinate origin is assumed to
            be the top-left corner).
        scale (Tensor): isotropic scale factor.

    Returns:
        Tensor: the affine matrix of 2D rotation.

    Shape:
        - Input: :math:`(B, 2)`, :math:`(B)` and :math:`(B)`
        - Output: :math:`(B, 2, 3)`

    Example:
        >>> center = torch.zeros(1, 2)
        >>> scale = torch.ones(1)
        >>> angle = 45. * torch.ones(1)
        >>> M = get_rotation_matrix2d(center, angle, scale)
        tensor([[[ 0.7071,  0.7071,  0.0000],
                 [-0.7071,  0.7071,  0.0000]]])
    """
    if not torch.is_tensor(center):
        raise TypeError("Input center type is not a torch.Tensor. Got {}"
                        .format(type(center)))

    if not (len(center.shape) == 2 and center.shape[1] == 2):
        raise ValueError("Input center must be a Bx2 tensor. Got {}"
                         .format(center.shape))

    # convert angle and apply scale
    scaled_rotation = angle_to_rotation_matrix(angle) * scale.view(-1, 1, 1)
    alpha= scaled_rotation[:, 0, 0]
    beta= scaled_rotation[:, 0, 1]

    # unpack the center to x, y coordinates
    x = center[..., 0]
    y= center[..., 1]

    # create output tensor
    batch_size= center.shape[0]
    M = torch.zeros(batch_size, 2, 3, device=center.device, dtype=center.dtype)
    M[..., 0:2, 0:2] = scaled_rotation
    M[..., 0, 2] = (torch.tensor(1.) - alpha) * x - beta * y
    M[..., 1, 2] = beta * x + (torch.tensor(1.) - alpha) * y
    return M







def _compute_rotation_matrix(angle: torch.Tensor,
                             center: torch.Tensor) -> torch.Tensor:
    """Computes a pure affine rotation matrix."""
    scale_tensor = torch.ones_like(angle)
    matrix_tensor = get_rotation_matrix2d(center, angle, scale)
    return matrix_tensor


def _compute_translation_matrix(translation: torch.Tensor) -> torch.Tensor:
    """Computes affine matrix for translation."""
    matrix_tensor = torch.eye( 3, device=translation.device, dtype=translation.dtype)
    matrix = matrix_tensor.repeat(translation.shape[0], 1, 1)

    dx, dy = torch.chunk(translation, chunks=2, dim=-1)
    matrix[..., 0, 2:3] += dx
    matrix[..., 1, 2:3] += dy
    return matrix


def _compute_scaling_matrix(scale: torch.Tensor,
                            center: torch.Tensor) -> torch.Tensor:
    """Computes affine matrix for scaling."""
    angle_tensor= torch.zeros_like(scale)
    matrix_tensor = get_rotation_matrix2d(center, angle_tensor, scale)
    return matrix_tensor


def _compute_shear_matrix(shear: torch.Tensor) -> torch.Tensor:
    """Computes affine matrix for shearing."""
    matrix_tensor = torch.eye(3, device=shear.device, dtype=shear.dtype)
    matrix = matrix_tensor.repeat(shear.shape[0], 1, 1)

    shx, shy = torch.chunk(shear, chunks=2, dim=-1)
    matrix[..., 0, 1:2] += shx
    matrix[..., 1, 0:1] += shy
    return matrix


# based on:
# https://github.com/anibali/tvl/blob/master/src/tvl/transforms.py#L166

def normal_transform_pixel(height, width):
    tr_mat = torch.Tensor([[1.0, 0.0, -1.0],[0.0, 1.0, -1.0],[0.0, 0.0, 1.0]])  # 1x3x3
    tr_mat[0, 0] = tr_mat[0, 0] * 2.0 / (width - 1.0)
    tr_mat[1, 1] = tr_mat[1, 1] * 2.0 / (height - 1.0)

    tr_mat = tr_mat.unsqueeze(0)

    return tr_mat


def dst_norm_to_dst_norm(dst_pix_trans_src_pix, dsize_src, dsize_dst):
    # source and destination sizes
    src_h, src_w = dsize_src
    dst_h, dst_w = dsize_dst
    # the devices and types
    device = dst_pix_trans_src_pix.device
    dtype = dst_pix_trans_src_pix.dtype
    # compute the transformation pixel/norm for src/dst
    src_norm_trans_src_pix = normal_transform_pixel(
        src_h, src_w).to(device).to(dtype)
    src_pix_trans_src_norm = torch.inverse(src_norm_trans_src_pix)
    dst_norm_trans_dst_pix = normal_transform_pixel(
        dst_h, dst_w).to(device).to(dtype)
    # compute chain transformations
    dst_norm_trans_src_norm = torch.matmul(
        dst_norm_trans_dst_pix, torch.matmul(
            dst_pix_trans_src_pix, src_pix_trans_src_norm))
    return dst_norm_trans_src_norm

def transform_points(trans_01: torch.Tensor,points_1: torch.Tensor) -> torch.Tensor:

    r"""Function that applies transformations to a set of points.
    Args:
        trans_01 (torch.Tensor): tensor for transformations of shape
          :math:`(B, D+1, D+1)`.
        points_1 (torch.Tensor): tensor of points of shape :math:`(B, N, D)`.
    Returns:
        torch.Tensor: tensor of N-dimensional points.
    Shape:
        - Output: :math:`(B, N, D)`

    Examples:

        >>> points_1 = torch.rand(2, 4, 3)  # BxNx3
        >>> trans_01 = torch.eye(4).view(1, 4, 4)  # Bx4x4
        >>> points_0 = transform_points(trans_01, points_1)  # BxNx3
    """
    if not torch.is_tensor(trans_01) or not torch.is_tensor(points_1):
        raise TypeError("Input type is not a torch.Tensor")
    if not trans_01.device == points_1.device:
        raise TypeError("Tensor must be in the same device")
    if not trans_01.shape[0] == points_1.shape[0]:
        raise ValueError("Input batch size must be the same for both tensors")
    if not trans_01.shape[-1] == (points_1.shape[-1] + 1):
        raise ValueError("Last input dimensions must differe by one unit")
    # to homogeneous
    points_1_h = torch.nn.functional.pad(points_1, [0, 1], "constant", 1.0)
    # transform coordinates
    points_0_h = torch.matmul(
        trans_01.unsqueeze(1), points_1_h.unsqueeze(-1))
    points_0_h = torch.squeeze(points_0_h, dim=-1)
    # to euclidean
    z_vec_tensor = points_0_h[..., -1:]
    mask_tensor = torch.abs(z_vec_tensor) >  1e-8
    scale_tensor= torch.ones_like(z_vec_tensor).masked_scatter_(mask_tensor, torch.tensor(1.0) / z_vec_tensor[mask_tensor])

    return scale_tensor * points_0_h[..., :-1]

def warp_grid(dst_homo_src: torch.Tensor,dsize) -> torch.Tensor:
    r"""Computes the grid to warp the coordinates grid by an homography.

    Args:
        dst_homo_src (torch.Tensor): Homography or homographies (stacked) to
                          transform all points in the grid. Shape of the
                          homography has to be :math:`(N, 3, 3)`.

    Returns:
        torch.Tensor: the transformed grid of shape :math:`(N, H, W, 2)`.
    """
    height, width = dsize
    grid = meshgrid(height, width, normalized_coordinates=True)

    batch_size= dst_homo_src.shape[0]
    device= dst_homo_src.device
    dtype= dst_homo_src.dtype
    # expand grid to match the input batch size
    grid_tensor = grid.expand(batch_size, -1, -1, -1)  # NxHxWx2
    if len(dst_homo_src.shape) == 3:  # local homography case
        dst_homo_src = dst_homo_src.view(batch_size, 1, 3, 3)  # NxHxWx3x3
    # perform the actual grid transformation,
    # the grid is copied to input device and casted to the same type
    flow_tensor = transform_points(dst_homo_src, grid_tensor.to(device).to(dtype))  # NxHxWx2
    return flow_tensor.view(batch_size, height, width, 2)  # NxHxWx2

def warp_affine(src: torch.Tensor,
                M: torch.Tensor,
                dsize: Tuple[int, int],
                mode: Optional[str] = 'bilinear',
                padding_mode: Optional[str] = 'zeros') -> torch.Tensor:
    r"""Applies an affine transformation to a tensor.

    The function warp_affine transforms the source tensor using
    the specified matrix:

    .. math::
        \text{dst}(x, y) = \text{src} \left( M_{11} x + M_{12} y + M_{13} ,
        M_{21} x + M_{22} y + M_{23} \right )

    Args:
        src (torch.Tensor): input tensor of shape :math:`(B, C, H, W)`.
        M (torch.Tensor): affine transformation of shape :math:`(B, 2, 3)`.
        dsize (Tuple[int, int]): size of the output image (height, width).
        mode (Optional[str]): interpolation mode to calculate output values
          'bilinear' | 'nearest'. Default: 'bilinear'.
        padding_mode (Optional[str]): padding mode for outside grid values
          'zeros' | 'border' | 'reflection'. Default: 'zeros'.

    Returns:
        torch.Tensor: the warped tensor.

    Shape:
        - Output: :math:`(B, C, H, W)`

    .. note::
       See a working example `here <https://github.com/arraiyopensource/
       kornia/blob/master/docs/source/warp_affine.ipynb>`__.
    """
    if not torch.is_tensor(src):
        raise TypeError("Input src type is not a torch.Tensor. Got {}"
                        .format(type(src)))
    if not torch.is_tensor(M):
        raise TypeError("Input M type is not a torch.Tensor. Got {}"
                        .format(type(M)))
    if not len(src.shape) == 4:
        raise ValueError("Input src must be a BxCxHxW tensor. Got {}"
                         .format(src.shape))
    if not (len(M.shape) == 3 or M.shape[-2:] == (2, 3)):
        raise ValueError("Input M must be a Bx2x3 tensor. Got {}"
                         .format(src.shape))
    try:
        # we generate a 3x3 transformation matrix from 2x3 affine
        M_3x3_tensor= F.pad(M, [0, 0, 0, 1, 0, 0], mode="constant", value=0)
        M_3x3_tensor[:, 2, 2] += 1.0

        dst_norm_trans_dst_norm =dst_norm_to_dst_norm(M_3x3_tensor, (src.shape[-2:]), dsize)
        # launches the warper
        return F.grid_sample(src, warp_grid(torch.inverse(dst_norm_trans_dst_norm),dsize=dsize), mode= 'bilinear', padding_mode= 'zeros')
    except Exception:
        PrintException()
        return None

def affine(tensor: torch.Tensor, matrix: torch.Tensor) -> torch.Tensor:
    r"""Apply an affine transformation to the image.

    Args:
        tensor (torch.Tensor): The image tensor to be warped.
        matrix (torch.Tensor): The 2x3 affine transformation matrix.

    Returns:
        torch.Tensor: The warped image.
    """
    # warping needs data in the shape of BCHW
    is_unbatched = tensor.ndimension() == 3
    if is_unbatched:
        tensor = torch.unsqueeze(tensor, dim=0)

    # we enforce broadcasting since by default grid_sample it does not
    # give support for that
    matrix = matrix.expand(tensor.shape[0], -1, -1)

    # warp the input tensor
    height = tensor.shape[-2]
    width = tensor.shape[-1]
    warped_tensor = warp_affine(tensor, matrix, (height, width))

    # return in the original shape
    if is_unbatched:
        warped = torch.squeeze(warped_tensor, dim=0)

    return warped_tensor


# based on:
# https://github.com/anibali/tvl/blob/master/src/tvl/transforms.py#L185

def rotate(tensor: torch.Tensor, angle: torch.Tensor) -> torch.Tensor:
    r"""Rotate the image anti-clockwise about the centre.

    See :class:`~kornia.Rotate` for details.
    """
    if not torch.is_tensor(tensor):
        raise TypeError("Input tensor type is not a torch.Tensor. Got {}"
                        .format(type(tensor)))
    if not torch.is_tensor(angle):
        raise TypeError("Input angle type is not a torch.Tensor. Got {}"
                        .format(type(angle)))

    if len(tensor.shape) not in (3, 4,):
        raise ValueError("Invalid tensor shape, we expect CxHxW or BxCxHxW. "
                         "Got: {}".format(tensor.shape))


    # compute the rotation matrix
    # TODO: add broadcasting to get_rotation_matrix2d for center
    angle = angle.expand(tensor.shape[0])
    center = torch.tensor([(tensor.size(4)-1)/2,(tensor.size(3)-1)/2]).expand(tensor.shape[0], -1).to(tensor.device)
    rotation_matrix = _compute_rotation_matrix(angle, center)

    # warp using the affine transform
    return affine(tensor, rotation_matrix[..., :2, :3])


def translate(tensor: torch.Tensor, translation: torch.Tensor) -> torch.Tensor:
    r"""Translate the tensor in pixel units.

    See :class:`~kornia.Translate` for details.
    """
    if not torch.is_tensor(tensor):
        raise TypeError("Input tensor type is not a torch.Tensor. Got {}"
                        .format(type(tensor)))
    if not torch.is_tensor(translation):
        raise TypeError("Input translation type is not a torch.Tensor. Got {}"
                        .format(type(translation)))
    if len(tensor.shape) not in (3, 4,):
        raise ValueError("Invalid tensor shape, we expect CxHxW or BxCxHxW. "
                         "Got: {}".format(tensor.shape))

    # compute the translation matrix
    translation_matrix = _compute_translation_matrix(translation)

    # warp using the affine transform
    return affine(tensor, translation_matrix[..., :2, :3])


def scale(tensor: torch.Tensor, scale_factor: torch.Tensor) -> torch.Tensor:
    r"""Scales the input image.

    See :class:`~kornia.Scale` for details.
    """
    if not torch.is_tensor(tensor):
        raise TypeError("Input tensor type is not a torch.Tensor. Got {}"
                        .format(type(tensor)))
    if not torch.is_tensor(scale_factor):
        raise TypeError("Input scale_factor type is not a torch.Tensor. Got {}"
                        .format(type(scale_factor)))

    # compute the tensor center

    # compute the rotation matrix
    # TODO: add broadcasting to get_rotation_matrix2d for center
    center = torch.tensor([(tensor.size(4) - 1) / 2, (tensor.size(3) - 1) / 2]).expand(tensor.shape[0], -1).to(tensor.device)
    scale_factor = scale_factor.expand(tensor.shape[0])
    scaling_matrix = _compute_scaling_matrix(scale_factor, center)

    # warp using the affine transform
    return affine(tensor, scaling_matrix[..., :2, :3])


def shear(tensor: torch.Tensor, shear: torch.Tensor) -> torch.Tensor:
    r"""Shear the tensor.

    See :class:`~kornia.Shear` for details.
    """
    if not torch.is_tensor(tensor):
        raise TypeError("Input tensor type is not a torch.Tensor. Got {}"
                        .format(type(tensor)))
    if not torch.is_tensor(shear):
        raise TypeError("Input shear type is not a torch.Tensor. Got {}"
                        .format(type(shear)))
    if len(tensor.shape) not in (3, 4,):
        raise ValueError("Invalid tensor shape, we expect CxHxW or BxCxHxW. "
                         "Got: {}".format(tensor.shape))

    # compute the translation matrix
    shear_matrix = _compute_shear_matrix(shear)

    # warp using the affine transform
    return affine(tensor, shear_matrix[..., :2, :3])


