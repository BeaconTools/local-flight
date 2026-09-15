import Svg, { Path, Rect } from "react-native-svg";
import { BEACON_FRAME_PATH } from "../theme/beaconBrand";

type BeaconToolsMarkProps = {
  size?: number;
  color?: string;
};

/** Decorative studio signature; the accompanying text supplies its name. */
export function BeaconToolsMark({ size = 18, color = "#a5bdff" }: BeaconToolsMarkProps) {
  return (
    <Svg width={size} height={size} viewBox="0 0 64 64" fill={color} accessible={false}>
      <Path d={BEACON_FRAME_PATH} />
      <Rect x={44} y={8} width={12} height={12} rx={3} />
    </Svg>
  );
}
