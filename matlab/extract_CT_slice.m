%function extract_CT_slice(X, Y, Z, Opacity)
% Inputs:
% Assuming you have X, Y, Z, and opacity arrays from the point cloud
fprintf('x range: %f, %f \n', min(X), max(X));
fprintf('y range: %f, %f \n', min(Y), max(Y));
fprintf('z range: %f, %f \n', min(Z), max(Z));
Z_slice = 20;             % The Z coordinate of the desired slice
px = 1;                   % Pixel size in X direction
py = 1;                   % Pixel size in Y direction
tolerance = 10;          % Tolerance for selecting Z slice points
method="scatteredInterpolant";
if method=="griddata"
    % Step 1: Select points close to the given Z_slice coordinate
    z_filter = abs(Z - Z_slice) < tolerance;  % Filter points in the Z slice range
    X_slice = X(z_filter);   % X coordinates of points in the slice
    Y_slice = Y(z_filter);   % Y coordinates of points in the slice
    Opacity_slice = Opacity(z_filter);  % Opacity of points in the slice
    
    % Step 2: Define the grid for interpolation
    x_min = min(X_slice);
    x_max = max(X_slice);
    y_min = min(Y_slice);
    y_max = max(Y_slice);
    
    % Define a grid for interpolation with pixel size
    [X_grid, Y_grid] = meshgrid(x_min:px:x_max, y_min:py:y_max);
    
    % Step 3: Interpolate using griddata
    image_grid = griddata(X_slice, Y_slice, Opacity_slice, X_grid, Y_grid, 'linear');
    
    % Step 4: Display the interpolated 2D image
    imagesc(x_min:px:x_max, y_min:py:y_max, image_grid);
    colormap(gray)
    colorbar
    axis equal;
    xlabel('X (mm)');
    ylabel('Y (mm)');
    title(['2D CT Slice at Z = ', num2str(Z_slice)]);
    colorbar;
elseif method=="scatteredInterpolant"
    % Step 1: Select points close to the given Z_slice coordinate
    z_filter = abs(Z - Z_slice) < tolerance;  % Filter points in the Z slice range
    X_slice = X(z_filter);   % X coordinates of points in the slice
    Y_slice = Y(z_filter);   % Y coordinates of points in the slice
    Opacity_slice = Opacity(z_filter);  % Opacity of points in the slice
    
    % Step 2: Define the grid for interpolation
    x_min = min(X_slice);
    x_max = max(X_slice);
    y_min = min(Y_slice);
    y_max = max(Y_slice);
    
    % Define a grid for interpolation with pixel size
    [X_grid, Y_grid] = meshgrid(x_min:px:x_max, y_min:py:y_max);
    
    % Step 3: Create scatteredInterpolant object and interpolate
    F = scatteredInterpolant(X_slice, Y_slice, Opacity_slice, 'nearest');
    image_grid = F(X_grid, Y_grid);
    
    % Step 4: Display the interpolated 2D image
    imagesc(x_min:px:x_max, y_min:py:y_max, image_grid);
    colormap(gray)
    colorbar
    axis equal;
    xlabel('X (mm)');
    ylabel('Y (mm)');
    title(['2D CT Slice at Z = ', num2str(Z_slice)]);
    colorbar;
elseif method=="histcounts2"
    % Inputs:
    % Assuming you have X, Y, Z, and opacity arrays from the point cloud
    Z_slice = 50;             % The Z coordinate of the desired slice
    px = 1;                   % Pixel size in X direction
    py = 1;                   % Pixel size in Y direction
    tolerance = 0.5;          % Tolerance for selecting Z slice points
    
    % Step 1: Select points close to the given Z_slice coordinate
    z_filter = abs(Z - Z_slice) < tolerance;  % Find points within tolerance
    X_slice = X(z_filter);   % X coordinates of points in the slice
    Y_slice = Y(z_filter);   % Y coordinates of points in the slice
    Opacity_slice = Opacity(z_filter);  % Opacity of points in the slice
    
    % Step 2: Define the grid for the 2D image based on pixel size and range
    x_min = min(X_slice);
    x_max = max(X_slice);
    y_min = min(Y_slice);
    y_max = max(Y_slice);
    
    % Create 2D grid for image (adjust size based on pixel size)
    x_edges = x_min:px:x_max;  % X axis grid based on pixel size
    y_edges = y_min:py:y_max;  % Y axis grid based on pixel size
    
    % Step 3: Convert 3D points to a 2D image grid using histcounts2
    % This bins the points into the defined grid and accumulates opacity
    [image_grid, ~, ~] = histcounts2(Y_slice, X_slice, y_edges, x_edges, 'Weight', Opacity_slice);
    
    % Step 4: Visualize the 2D CT slice image
    imagesc(x_edges, y_edges, image_grid);  % Display the 2D image
    colormap(gray)
    colorbar
    axis equal;
    xlabel('X (mm)');
    ylabel('Y (mm)');
    title(['2D CT Slice at Z = ', num2str(Z_slice)]);
    colorbar;
end