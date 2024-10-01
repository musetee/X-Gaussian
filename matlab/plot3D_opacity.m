load_from_path = 1;
if load_from_path==1
    clear
    object = 'foot';
    object = strcat(object, '_no_norm');
    input_path = 'G:\projects\X-Gaussian\output\';
    path=strcat(input_path, object, '\');
    load([path, object],'points');
end 
points_number = size(points,1);
X=points(:,1);
Y=points(:,2);
Z=points(:,3);
Opacity = points(:,4);
fprintf('Opacity range: %f, %f \n', min(Opacity), max(Opacity));

X = double(X);
Y = double(Y);
Z = double(Z);
Opacity = double(Opacity);

Threshold1 = -6;
Threshold2 = 8;
Threshold3 = 10;
Opacity_filter_1 = Opacity < Threshold1;
Opacity_filter_2 = (Opacity >= Threshold1) & (Opacity < Threshold2);
Opacity_filter_3 = (Opacity >= Threshold2) & (Opacity <= Threshold3);
Opacity_filter_4 = Opacity >= Threshold3;

max_Opacity = max(Opacity);
min_Opacity = min(Opacity);
Opacity_minmax_norm = (Opacity-min_Opacity)/(max_Opacity-min_Opacity);

% Define color for the points (you can choose a colormap or specify RGB values)
Color = zeros(points_number,3); % repmat(Opacity, 1, 3); %gray(points_number);    % Using jet or gray colormap for coloring

% Define RGB colors for different ranges
% 0 0 0 black
% 1 1 1 white
% 1 0 0 red
% 0 0 1 blue
% 1 1 0 yellow
% 0 1 0 green
% 1 0 1 purple
Colors(Opacity_filter_1, :) = repmat([1, 1, 1], sum(Opacity_filter_1), 1); %  for Range 1
Colors(Opacity_filter_2, :) = repmat([0, 0, 0], sum(Opacity_filter_2), 1); % Green for Range 2
Colors(Opacity_filter_3, :) = repmat([1, 1, 1], sum(Opacity_filter_3), 1); % Blue for Range 3
Colors(Opacity_filter_4, :) = repmat([1, 1, 1], sum(Opacity_filter_4), 1); % Yellow for Range 4

figure()
% Plotting the 3D points
s = scatter3(X, Y, Z, 10, Colors, 'filled');

s.AlphaData = Opacity_minmax_norm;
s.MarkerFaceAlpha = 'flat';

% Set up transparency (opacity)
% Use 'alpha' to control transparency based on your Opacity array
% alpha(gca, 'scaled');
% set(gca, 'ALim', [0 1]);
% h = get(gca, 'Children'); % get scatter property
% set(h, 'MarkerFaceAlpha', 'flat');
% set(h, 'AlphaData', Opacity, 'AlphaDataMapping', 'scaled'); % Opacity , 'EdgeAlpha', 'interp'

% Adjust view and axis
xlabel('X');
ylabel('Y');
zlabel('Z');
view(3);  % Set to 3D view
%axis vis3d;  % Lock aspect ratio for better visualization
grid on;

figure()
hist(Opacity,100);
